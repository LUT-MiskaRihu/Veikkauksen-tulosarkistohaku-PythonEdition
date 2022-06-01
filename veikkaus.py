import requests
import json
import sys
import datetime
import mrprintlib as mrp
import mrmsglib as mrm
import mrpromptlib as mpl

DATE_FORMAT = "{day:02}.{month:02}.{year}"
CSV_LINE = "{date};{primary};{secondary}"



week_min = 1
week_max = 52

lang = 0

class ENTRY:
    timestamp = None
    primary = []
    secondary = []


# def lang():
#     return int(mrm.LANGUAGES.index(lang))


def mainMenu():
    min = 0
    max = 1

    print("1) Hae vanhat lottotulokset.")
    print("0) Lopeta")

    while (True):
        selection = mpl.askForInteger("Valintasi")
        if ((selection != None) and (min <= selection <= max)):
            break
        print(mrm.ERR_UNKNOWN_SELECTION[lang])
    
    return selection


def makeURL(year, week):
    url = "https://www.veikkaus.fi/"\
                  "api/"                    \
                  "draw-results/"           \
                  "v1/"                     \
                  "games/"                  \
                  "LOTTO/"                  \
                  "draws/"                  \
                  "by-week/"                \
                  "{year}-W{week:02}"       \
                  .format(year=year, week=week)
    return url


def parseJSON(url):
    string = requests.get(url).text
    parsed = json.loads(string)
    return parsed


def extractResults(json_data):
    # Read information
    timestamp = json_data[0]["drawTime"]
    results = json_data[0]["results"]
    primary = results[0]["primary"]
    secondary = results[0]["secondary"]

    # Create new entry
    entry = ENTRY()
    entry.timestamp = datetime.datetime.fromtimestamp(timestamp / 1e3)
    entry.primary = primary
    entry.secondary = secondary
    return entry


def getFilenameFromUser():
    return mpl.askForString("Enter a filename (without the extension)").upper()


def writeFile(filename, entries):
    #filename = "tulokset-" + ".CSV"
    
    mrp.pinfo("Writing results to a file")
    try:
        with open(filename, "w", encoding="utf-8") as file:
            # Write headers.
            file.write(
                CSV_LINE.format(
                    date="Arvontapäivä",
                    primary="Päänumerot",
                    secondary="Sivunomerot"
                )
            )
            file.write('\n')

            # Write entries
            for entry in entries:
                date = DATE_FORMAT.format(
                    year=entry.timestamp.year,
                    month=entry.timestamp.month,
                    day=entry.timestamp.day
                )
                #date = str(entry.timestamp)
                line = CSV_LINE.format(
                    date=date,
                    primary=str(entry.primary).replace("'", ""),
                    secondary=str(entry.secondary).replace("'", "")
                )
                file.write(line + '\n')

    except FileNotFoundError as e:
        mrp.perror("Failed to write the file")
        mrp.perror(mrm.ERR_FILE_NOT_FOUND[lang].format(filename))
        sys.exit(1)
    
    mrp.pinfo("Finished writing the file.")


def getResults():
    year_min = mpl.askForInteger("Haun alaraja (vuosi)")
    year_max = mpl.askForInteger("Haun yläraja (vuosi)")

    for y in range(year_min, year_max+1):
        mrp.pinfo("Started fetching data for year {0}".format(y))
        entries = []
        for w in range(week_min, week_max+1):
            url = makeURL(y, w)
            data = parseJSON(url)
            entry = extractResults(data)
            entries.append(entry)
            #mrp.pinfo("Fetched data from {0}".format(url))
            print(y, w, end="\r")
        filename = "tulokset-{year}.csv".format(year=y)
        writeFile(filename, entries)


def main():
    while (True):
        selection = mainMenu()

        if (selection == 0):
            print(mrm.INFO_QUIT[lang])
            break
        elif (selection == 1):
            getResults()
        
        print()
        print()


main()

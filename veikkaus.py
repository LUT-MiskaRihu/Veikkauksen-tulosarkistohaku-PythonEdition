# Veikkaus Results Archive Search and Analyze Tool
#
# Author:   Miska Rihu
# Github:   https://github.com/LUT-MiskaRihu/
# License:  
# Modified: 
import requests
import json
import sys
import datetime
import statistics
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
    max = 4

    print("1) Hae lottotulokset internetistä")
    print("2) Hae lottotulokset tiedostosta")
    print("3) Analysoi tulokset")
    print("4) Tallenna ")
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


def clearLine():
    print(79*' ', end='\r')


def getFilenameFromUser():
    return mpl.askForString("Enter a filename (without the extension)").upper()


def writeFile(filename, entries):
    #filename = "tulokset-" + ".CSV"
    
    mrp.pinfo("Writing results to a file '{file}'".format(file=filename))
    try:
        with open(filename, "w", encoding="utf-8") as file:
            # Write headers.
            file.write(
                CSV_LINE.format(
                    date="Arvontapäivä",
                    primary="Päänumerot",
                    secondary="Lisänumerot"
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
                    primary=entry.primary,
                    secondary=entry.secondary
                )
                file.write(line + '\n')

    except FileNotFoundError as e:
        mrp.perror("Failed to write the file '{file}'".format(file=filename))
        sys.exit(1)
    
    mrp.pinfo("Finished writing the file '{file}'".format(file=filename))


def getResultsOnline(save_each_year_separately):
    total_progress = 0
    all_entries = []
    year_min = mpl.askForInteger("Upper limit (year)")
    year_max = mpl.askForInteger("Lower limit (year)")
    count_years = year_max - year_min + 1
    count_weeks = 52
    count_total_entries = count_years * count_weeks

    for y in range(year_min, year_max+1):
        entries = []
        yearly_progress = 0
        mrp.pinfo("Started fetching data for year {0}".format(y))

        for w in range(week_min, week_max+1):
            url = makeURL(y, w)
            data = parseJSON(url)
            entry = extractResults(data)
            entries.append(entry)
            yearly_progress += 1
            total_progress +=1
            print(
                "Yearly progress: {yearly:3.2f} %"  \
                " | "                               \
                "Total progress: {total:3.2f} %"    \
                .format(
                    yearly=yearly_progress/count_weeks*100,
                    total=total_progress/count_total_entries*100
                ),
                end='\r'
            )
        
        all_entries.extend(entries)
        clearLine()

        if (save_each_year_separately):
            filename = "results-{year}.csv".format(year=y)
            writeFile(filename, entries)
    
    mrp.pinfo("Finished fetching data")
    return all_entries


def getResultsOffline():
    mrp.perror("This feature is not implemented yet")
    return []


def analyzeResults(entries):
    primary_counts = []
    secondary_counts = []
    p_total = 0
    s_total = 0
    p_mode = 0
    s_mode = 0
    p_mode_percent = 0
    s_mode_percent = 0

    for entry in entries:
        primary_counts.extend(entry.primary)
        secondary_counts.extend(entry.secondary)

    
    csv_string = "Nro;Päänumerona (kpl);Lisänumerona (kpl);Päänumerona (%);Lisänumerona (kpl)\n"
    for i in range(47):
        number = i + 1
        p_count = primary_counts.count(number)
        p_total = len(primary_counts)
        p_percent = p_count / p_total * 100
        s_count = secondary_counts.count(number)
        s_total = len(secondary_counts)
        s_percent = s_count / s_total * 100
        line = "{num};{p_count};{s_count};{p_percent:.2f};{s_percent:.2f}\n"
        line = line.format(
            num=number,
            p_count=p_count,
            s_count=s_count,
            p_percent=p_percent,
            s_percent=s_percent
        )
        csv_string += line

    p_mode = statistics.mode(primary_counts)
    s_mode = statistics.mode(secondary_counts)
    p_mode_percent = primary_counts.count(p_mode) / p_total * 100
    s_mode_percent = secondary_counts.count(s_mode) / s_total * 100

    print()
    print(csv_string, end="")

    print()
    print("The mode of the primary numbers was {num} ({percent} %).".format(
            num=p_mode,
            percent=p_mode_percent
        )
    )
    print("The mode of the secondary numbers was {num} ({percent} %).".format(
            num=s_mode,
            percent=s_mode_percent
        )
    )

    return csv_string


def saveResults():
    mrp.perror("This feature is not implemented yet")
    return []


def main():
    entries = []
    analysis = ""

    while (True):
        selection = mainMenu()

        if (selection == 0):
            print(mrm.INFO_QUIT[lang])
            break

        elif (selection == 1):
            while (True):
                separate_files = input("Save each year to a separate file? (y/n): ").lower()
                if (separate_files == "y"):
                    separate_files = True
                    break
                elif (separate_files == "n"):
                    separate_files = False
                    break
                else:
                    print(mrm.ERR_UNKNOWN_SELECTION[lang])
            entries = getResultsOnline(separate_files)
        
        elif (selection == 2):
            entries = getResultsOffline()
        
        elif (selection == 3):
            if (len(entries) < 1):
                print("No entries found, run the search first.")
                entries = getResultsOnline()
            analysis = analyzeResults(entries)
        
        elif (selection == 4):
            if (len(analysis) < 1):
                mrp.perror("Analysis must be done first")
            else:
                saveResults()

        print()
        print()


main()

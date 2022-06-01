# Common Messages Library
#
# Author:   Miska Rihu
# Modified: 2022-06-01
##############################################################################

# Languages
LANGUAGES = ["en", "fi"]


# Messages
ERR_FILE_NOT_FOUND = ["File '{file}' not found: ", "Tiedostoa '{file}' ei löydy: "]
ERR_UNKNOWN_SELECTION = ["Unknown selection, try again: ", "Tuntematon valinta, yritä uudelleen: "]
ERR_NOT_INTEGER = ["'{value}' is not an integer", "'{value}' ei ole kokonaisluku"]
INFO_QUIT = ["Thank you for using this program.", "Kiitos ohjelman käytöstä."]

# Get numeric language code
def langNum(lang):
    return LANGUAGES.index(lang)
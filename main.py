from Common import *
from Spreadsheet import Spreadsheet

from Android import *
from IOS import *

import sys
import gspread
# TODO: oauth2client is deprecated. Use recommended google-auth
from oauth2client.service_account import ServiceAccountCredentials

USAGE = """
Usage: {0} /path/to/google_credentials.json SPREADSHEET_NAME TARGET
    
    SPREADSHEET_NAME
        If it contains whitespaces, use '' around the name.

    TARGET
        Valid options are: 'android', 'ios', 'ios-swift'
"""

# Make sure we have all necessary parameters specified at command line.
if (len(sys.argv) < 4):
    print(USAGE.format(sys.argv[0]))
    sys.exit(1)
# Parse command line arguments.
credentialsFileName = sys.argv[1]
documentName = sys.argv[2]
targetName = sys.argv[3]

print("Connecting to Google Sheets API")
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(credentialsFileName, scope)
client = gspread.authorize(credentials)

print("Opening spreadsheet")
spreadsheet = Spreadsheet(client)
spreadsheet.open(documentName)

print("Reading configuration page")
cfgPage = spreadsheet.sheet("CFG")
cfg = configurationFromPage(cfgPage)

print("Reading source page")
srcPage = spreadsheet.sheet("SRC")
(languages, translations) = parsePage(srcPage, cfg)

print("Found languages: '{0}'".format(languages))

if (targetName == "android"):
    androidGenerateLocalizationFiles(translations, languages)
elif (targetName == "ios"):
    iosGenerateLocalizationFiles(translations, languages)
    iosGenerateConstantsFiles(translations, languages)
elif (targetName == "ios-swift"):
    iosGenerateLocalizationFiles(translations, languages)
    iosGenerateSwiftConstantsFile(translations, languages)
else:
    print("ERROR: Unknown target")
    sys.exit(1)


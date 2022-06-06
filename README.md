# courier
Script to automate transferral from one Google Spreadsheet to another.


## Requirements:
The following packages are required to install for this script to work.
- gspread

In addition, please create and add a Google Cloud service account to gspread configuration file AND share your spreadsheets with the service account.



## Config
Script utilizes a target spreadsheet and a reference spreadsheet, labeled "target" and "ref" respectively in configuration file.
Please enter the **full** name of your spreadsheets.

This also applies to the worksheets in the configuration file.


## Future updates
Future updates will see program carry over modularity by moving indexing spreadsheet schema to configuration file.

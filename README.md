# Phantom-PasteBin

An add-on app for [Phantom](https://www.phantom.us/) that implements an investigative action of 'fetch paste' to be triggered by email alerts sent from PasteBin.

The 'fetch paste' action downloads the paste referenced in the alert email and saves it to the Phantom vault. A widget is also created to display the PasteID, creation time, title author and matching keyword that triggered the alert. A text box in the widget also displays the lines from the paste that matched the keywords.

## Installation and Configuration

### Manual Installation

1. Admin -> Apps and click the "+ APP" button to add a new app
2. Choose the 'pastebin.tgz' file and click install

### Configuration
1. Click the "Assets" tab and click on the "rest - incident" asset. On the "Ingest Settings" tab copy the values for the ph-auth-token.
2. Now click back to the "Assets" section and click the "+ ASSET" button.

- On the "Asset Definition" tab:
1. Asset Name: PasteBin
2. Vendor: PasteBin (should autofill the product field)
- On the "Asset Settings" tab:
1. Phantom Server IP/Hostname: Should be able to leave this set at 127.0.0.1
2. Phantom REST API token: Paste in the value of 'ph-auth-token' that you copied from the 'rest - incident' asset
3. Click save


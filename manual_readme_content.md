## Port Details

The app uses HTTP/ HTTPS protocol for communicating with the PasteBin server. Below are the default
ports used by the Splunk SOAR Connector.

| SERVICE NAME | TRANSPORT PROTOCOL | PORT |
|--------------|--------------------|------|
| http | tcp | 80 |
| https | tcp | 443 |

## Steps to Configure the PasteBin Splunk SOAR app's asset

Follow these steps to configure the PasteBin Splunk SOAR app's asset:

- Log in to the PasteBin platform.

  - Once logged in, select **API** by clicking it from the navigation bar.
  - In the Developers API section, click on **Your Unique Developer API Key** .
  - Copy the generated Developers API Key.
  - NOTE: Whenever you log in, the generated API key will always be available
    [here](https://pastebin.com/doc_api) .

- Now, Log in to your Splunk SOAR instance.

  - Navigate to the **Home** dropdown and select **Apps** .
  - Search the PasteBin App from the search box.
  - Click on the **CONFIGURE NEW ASSET** button.
  - Navigate to the **Asset Info** tab and enter the Asset name and Asset description.
  - Navigate to the **Asset Settings** .
  - Paste the generated **API Key** from PasteBin UI to its respective configuration parameter.
  - Pastebin username and password are optional parameters. To create any paste as user, you
    need to provide credentials for the same.
  - Save the asset.
  - Now, test the connectivity of the Splunk SOAR server to the PasteBin instance by clicking
    the **TEST CONNECTIVITY** button.

## Explanation of the Asset Configuration Parameters

The asset configuration parameters affect 'test connectivity' and some other actions of the
application. The parameters related to test connectivity action are API Key, Pastebin username, and
Pastebin password.

- **Pastebin api dev key (Required):** API Token for asset authorization.
- **Pastebin username (Optional):** The username of your PasteBin account.
- **Pastebin password (Optional):** The password of your PasteBin account.
- NOTE: The developer API key, username, and password, all must belong to one particular account
  to create paste as a user.

## Explanation of the PasteBin Actions' Parameters

- ### Test Connectivity (Action Workflow Details)

  - This action will test the connectivity of the Splunk SOAR server to the PasteBin instance by
    making an initial API call using the provided asset configuration parameters.
  - The action validates the provided asset configuration parameters. Based on the API call
    response, the appropriate success and failure message will be displayed when the action gets
    executed.

- ### Get Data

  To download, parse, and save a paste from PasteBin, the user can run this action. After a
  successful run of the action, the text file will be generated with paste data and stored in the
  vault.\
  [![](img/get_data_details.png)](img/get_data_details.png)

  - **Action Parameter** : Pastebin URL

    This is a required parameter. The user can enter any Pastebin URL to fetch its details. On
    running the action, it generates a custom view listing paste details like author, created
    time, title, paste data, etc. Fetching details for the 'Private as user' paste is not
    supported by this action.

  - **NOTE:** While creating a paste from the PasteBin platform where we have set the paste
    format (syntax highlighting) in Bash, C, C#, C++, CSS, HTML, JSON, Java, JavaScript, Lua,
    Objective C, PHP, Perl, Python, Ruby, and Swift, file will be downloading the paste in
    'paste_title.file_extension' format if title is provided else it will be downloaded in
    'paste_id.file_extension' format. For all the other syntax highlighting, the file will be
    downloaded in 'paste_title.txt' format if title is provided, else it will be downloaded in
    'paste_id.txt' format.\
    While running the 'get_data' action, all the paste_format (syntax highlighting) which have
    been selected will be stored in the 'paste_id.txt' format

- ### Create Paste

  This action lets a user create a paste from pastebin.

  - **Action Parameter: Paste text**

    - This is a required parameter. It is the text that will be written inside your paste.

  - **Action Parameter: Paste title**

    - This is an optional parameter. It will be the name/title of your paste.

  - **Action Parameter: Paste format**

    - This is an optional parameter. It will be the syntax highlighting value. This parameter
      supports more than 200 types of syntax highlighting options like Python, C, SQL, etc.

  - **Action Parameter: Paste exposure**

    - This is an optional parameter. It will set the exposure of a paste by making it a
      public, unlisted, or private paste.

  - **Action Parameter: Paste expiration**

    - This is an optional parameter. It will set the expiration date of any paste according to
      the choice of the user.

  - **Action Parameter: Paste as user**

    - This is an optional parameter. The paste will be pasted as 'User' (Pastebin username) if
      this parameter is marked check, else it will be pasted as 'Guest'. Creating a 'Private
      as user' paste is not supported by this action.

import phantom.app as phantom
from phantom.base_connector import BaseConnector
from phantom.action_result import ActionResult
from phantom.vault import Vault
import simplejson as json

from django.utils.encoding import smart_str
from bs4 import BeautifulSoup
from urlparse import urlparse
from dateutil.parser import parse
import os
import uuid
import pytz
import requests
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()


class PasteBinConnector(BaseConnector):

    def _convert_to_client_tz(self, t_str):
        # TODO: Next version will have a configurable TZ
        t = parse(t_str, tzinfos={"CDT": -18000, "CST": -21600})
        client_tz = pytz.UTC

        # try:
        #    client_tz = pytz.timezone("EST5EDT")
        # except:
        #    client_tz = pytz.UTC
        return t.astimezone(pytz.timezone(client_tz.zone)).strftime("%Y-%m-%d %H:%M:%S %Z")

    def _get_pastebin_keyword(self, container_id):

        config = self.get_config()
        headers = {"ph-auth-token": str(config['phantom_rest_api_token'])}
        phantom_base_url = self.get_phantom_base_url()

        try:
            resp = requests.get(phantom_base_url + "/rest/container/{}".format(container_id), headers=headers, verify=False)
            cntnr_json = resp.json()
            keyword = cntnr_json['name'].split("keyword: ", 1)[1]
            return (keyword)
        except Exception as e:
            return ("ERROR: {0}".format(e))

    def _parse_paste(self, keyword, raw_paste):
        matching_lines = []

        for line in raw_paste.splitlines():
            idx = line.lower().find(keyword)

            if idx > -1:
                matching_lines.append(line)

        return matching_lines

    def _add_file_to_vault(self, file_name, container_id, file_data):

        success = True

        if hasattr(Vault, 'get_vault_tmp_dir'):
            temp_dir = Vault.get_vault_tmp_dir()
        else:
            temp_dir = "opt/phantom/vault/tmp"

        temp_dir = temp_dir + '/{}'.format(uuid.uuid4())
        os.makedirs(temp_dir)
        fname = os.path.join(temp_dir, file_name)

        try:
            with open(fname, "w") as outfile:
                outfile.write(smart_str(file_data))
        except IOError:
            success = False

        if success:
            Vault.add_attachment(fname, container_id, file_name=None, metadata=dict())

    def _handle_fetch_paste(self, param):

        container_id = self.get_container_id()

        # TODO: Add support for rare occassion of multiple URLs in an alert:
        pasteid = urlparse(param['paste_url']).path.strip('/')

        action_result = ActionResult(dict(param))
        self.add_action_result(action_result)

        try:
            self.save_progress("Fetching paste with ID {0}".format(pasteid))
            results = requests.get("https://pastebin.com/{0}".format(pasteid), verify=True)
        except Exception as e:
            action_result.set_status(phantom.APP_ERROR, "Failed to download paste: ", e)
            return action_result.get_status()

        try:
            self.save_progress("Parsing Magic {0}".format(pasteid))
            soup = BeautifulSoup(results.content, 'html.parser')

            if soup.title.string == 'Pastebin.com - Page Removed':
                action_result.add_data({'pasteid': pasteid,
                    'creation_time': "N/A",
                    'author': "N/A",
                    'title': "This page has been removed!",
                    'contents': "This page is no longer available. It has either expired, been removed by its creator, or removed by one of the Pastebin staff."})
            else:
                paste_title = soup.find("div", class_="paste_box_line1").string
                paste_author = soup.find("div", class_="paste_box_line2").a.string if soup.find("div", class_="paste_box_line2").a else 'Guest'
                paste_time = soup.find("div", class_="paste_box_line2").span['title']
                paste_time = self._convert_to_client_tz(paste_time)
                paste_data = soup.find("textarea", class_="paste_code").string

                self.save_progress("Finding keywords")

                keyword = self._get_pastebin_keyword(container_id)
                keyword_matches = self._parse_paste(keyword, paste_data)

                action_result.add_data({'pasteid': pasteid, 'creation_time': paste_time,
                    'author': paste_author, 'title': paste_title, 'keyword': keyword, 'contents': '\n'.join(keyword_matches) })

                self.save_progress("Saving paste to vault...")
                self._add_file_to_vault(pasteid + '.txt', container_id, paste_data)

        except Exception as e:
            action_result.set_status(phantom.APP_ERROR, 'Failed to parse paste:', e)
            return action_result.get_status()

        # Used for debugging
        action_result.update_summary({'Msg': "{0}".format('Finished')})

        action_result.set_status(phantom.APP_SUCCESS)

        return phantom.APP_SUCCESS

    def _handle_test_connectivity(self, param):

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        # NOTE: test connectivity does _NOT_ take any parameters
        # i.e. the param dictionary passed to this handler will be empty.
        # Also typically it does not add any data into an action_result either.
        # The status and progress messages are more important.

        try:
            self.save_progress("Connecting to endpoint")
            results = requests.get("https://pastebin.com/caCMuQtT", verify=True)

            soup = BeautifulSoup(results.content, 'html.parser')
            if soup.title.string == "Phantom Test Paste - Pastebin.com":
                self.save_progress("Test Connectivity Passed")
                return action_result.set_status(phantom.APP_SUCCESS)
            else:
                return action_result.set_status(phantom.APP_ERROR, "Test Connectivity Failed")

        except Exception as e:
            action_result.set_status(phantom.APP_ERROR, "Test Connectivity Failed", e)
            return action_result.get_status()

    def handle_action(self, param):
       ret_val = phantom.APP_SUCCESS
       actn_req = self.get_action_identifier()
       self.debug_print("action_id", self.get_action_identifier())

       if actn_req == 'get_data':
           ret_val = self._handle_fetch_paste(param)

       elif actn_req == 'test_connectivity':
           ret_val = self._handle_test_connectivity(param)

       return ret_val


if __name__ == '__main__':

    import sys
    import pudb
    pudb.set_trace()

    if (len(sys.argv) < 2):
        print "No test json specified as input"
        exit(0)

    with open(sys.argv[1]) as f:
        in_json = f.read()
        in_json = json.loads(in_json)
        print(json.dumps(in_json, indent=4))

        connector = PasteBinConnector()
        connector.print_progress_message = True
        ret_val = connector._handle_action(json.dumps(in_json), None)
        print (json.dumps(json.loads(ret_val), indent=4))

    exit(0)

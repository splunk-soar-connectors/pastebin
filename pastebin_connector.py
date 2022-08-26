# File: pastebin_connector.py
#
# Copyright (c) 2016-2022 Splunk Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions
# and limitations under the License.
#
#
# Python 3 Compatibility imports
from __future__ import print_function, unicode_literals

import os
import urllib.parse
import uuid
from urllib.parse import urlparse

import phantom.app as phantom
import phantom.rules as ph_rules
import pytz
import requests
import simplejson as json
from bs4 import BeautifulSoup
from dateutil.parser import parse
from django.utils.encoding import smart_str
from phantom.action_result import ActionResult
from phantom.base_connector import BaseConnector
from phantom.vault import Vault

from pastebin_consts import *

requests.packages.urllib3.disable_warnings()


class RetVal(tuple):
    def __new__(cls, val1, val2=None):
        return tuple.__new__(RetVal, (val1, val2))


class PasteBinConnector(BaseConnector):

    def __init__(self):
        """Initialize global variables."""
        # Call the BaseConnectors init first
        super(PasteBinConnector, self).__init__()

        self._state = {}
        self._user_key = ""
        self._api_key = ""
        self._pastebin_username = ""
        self._pastebin_password = ""

    def _convert_to_client_tz(self, t_str):
        # TODO: Next version will have a configurable TZ
        t = parse(t_str, tzinfos={"CDT": -18000, "CST": -21600})
        client_tz = pytz.UTC

        # try:
        #    client_tz = pytz.timezone("EST5EDT")
        # except:
        #    client_tz = pytz.UTC
        return t.astimezone(pytz.timezone(client_tz.zone)).strftime("%Y-%m-%d %H:%M:%S %Z")

    def _add_file_to_vault(self, action_result, file_name, container_id, file_data):
        # action_result = ActionResult(dict(param))
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
            # Vault.add_attachment(fname, container_id, file_name=None, metadata=dict())
            # Save attachment file to the vault\
            try:
                success, message, attachment_vault_id = ph_rules.vault_add(
                    container=container_id,
                    file_location=fname,
                    file_name=None
                )
                if not success:
                    return action_result.set_status(phantom.APP_ERROR, message)
                action_result.add_data({"vault_id": attachment_vault_id})

            except Exception as e:
                error_msg = "Unable to add file to the vault for attachment name: {0}. Error: {1}".format(
                    fname, self._get_error_message_from_exception(e))
                return action_result.set_status(phantom.APP_ERROR, error_msg)

    def _get_error_message_from_exception(self, e):
        """This function is used to get appropriate error message from the exception.
        :param e: Exception object
        :return: error message
        """
        error_msg = PASTEBIN_ERROR_MESSAGE
        error_code = PASTEBIN_ERROR_CODE_MESSAGE
        try:
            if hasattr(e, "args"):
                if len(e.args) > 1:
                    error_code = e.args[0]
                    error_msg = e.args[1]
                elif len(e.args) == 1:
                    error_code = PASTEBIN_ERROR_CODE_MESSAGE
                    error_msg = e.args[0]
        except Exception as ex:
            self.debug_print("Exception: {}".format(ex))
            pass

        if not error_code:
            error_text = "Error Message: {}".format(error_msg)
        else:
            error_text = PASTEBIN_ERROR_MESSAGE_FORMAT.format(error_code, error_msg)

        return error_text

    def _process_html_response(self, response, action_result):
        resp_txt = response.text
        status_code = response.status_code

        if 200 <= response.status_code < 399:
            return RetVal(phantom.APP_SUCCESS, resp_txt)

        if status_code == 403 or 404:
            try:
                soup = BeautifulSoup(response.text, "html.parser")
                # Remove the script, style, footer and navigation part from the HTML message
                for element in soup(["script", "style", "footer", "nav"]):
                    element.extract()
                error_text = soup.text
                split_lines = error_text.split("\n")
                split_lines = [x.strip() for x in split_lines if x.strip()]
                error_message = "\n".join(split_lines)
            except Exception:
                error_message = "Cannot parse error details"

        if status_code in [401, 422]:
            error_message = resp_txt

        if status_code == 500:
            error_message = "Internal Server Error"

        message = "Status Code: {0}. Data from server:\n{1}\n".format(
            status_code, error_message
        )
        message = message.replace("{", "{{").replace("}", "}}")
        return RetVal(action_result.set_status(phantom.APP_ERROR, message), None)

    def _process_empty_response(self, response, action_result):
        if response.status_code == 200:
            return RetVal(phantom.APP_SUCCESS, {})

        return RetVal(
            action_result.set_status(
                phantom.APP_ERROR, "Empty response and no information in the header"
            ),
            None,
        )

    def _process_response(self, r, action_result):
        # store the r_text in debug data, it will get dumped in the logs if the action fails
        if hasattr(action_result, "add_debug_data"):
            action_result.add_debug_data({"r_status_code": r.status_code})
            action_result.add_debug_data({"r_text": r.text})
            action_result.add_debug_data({'r_headers': r.headers})

        if "html" in r.headers.get("Content-Type", ""):
            return self._process_html_response(r, action_result)

        if not r.text:
            return self._process_empty_response(r, action_result)

        message = "Can't process response from server. Status Code: {0} Data from server: {1}".format(
            r.status_code, r.text.replace("{", "{{").replace("}", "}}")
        )

        return RetVal(action_result.set_status(phantom.APP_ERROR, message), None)

    def _make_rest_call(
        self,
        url,
        action_result,
        headers=None,
        timeout=60,
        data=None,
        method="get",
        **kwargs
    ):

        resp_json = None
        try:
            request_func = getattr(requests, method)
        except AttributeError:
            return action_result.set_status(phantom.APP_ERROR, "Invalid method: {0}".format(method)), resp_json
        try:
            requests_response = request_func(
                url,
                headers=headers,
                data=data,
                timeout=DEFAULT_TIMEOUT_SECONDS,
                **kwargs,
            )
        except Exception as e:
            return action_result.set_status(
                phantom.APP_ERROR, "Error connecting to server. Details: {0}".format(self._get_error_message_from_exception(e))), resp_json

        return self._process_response(requests_response, action_result)

    def _handle_test_connectivity(self, param):

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))
        self.save_progress(PASTEBIN_CONNECTION_MSG)

        api_paste_code = "Test connectivity checked"

        ret_val, _ = self._creating_paste(
            action_result,
            self._api_key,
            api_paste_code
        )
        if phantom.is_fail(ret_val):
            self.save_progress(PASTEBIN_CONNECTIVITY_FAIL_MSG)
            return action_result.get_status()

        self.save_progress(PASTEBIN_CONNECTIVITY_PASS_MSG)
        return action_result.set_status(phantom.APP_SUCCESS)

    def _get_user_key(self, action_result, pastebin_username, pastebin_password):
        url = GET_USER_KEY_URL
        payload = PASTEBIN_GET_USER_KEY_PAYLOAD.format(
            self._api_key,
            pastebin_username,
            pastebin_password
        )
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        ret_val, response = self._make_rest_call(
            url=url,
            action_result=action_result,
            headers=headers,
            data=payload,
            timeout=30,
            method="post"
        )
        if phantom.is_fail(ret_val):
            return action_result.get_status(), None

        return action_result.set_status(phantom.APP_SUCCESS, "User key obtained successfully"), response

    def _creating_paste(
        self,
        action_result,
        api_key,
        api_paste_code,
        api_option="paste",
        api_user_key="",
        api_paste_name="",
        api_paste_format="",
        api_paste_exposure="",
        api_paste_expiration=""
    ):
        url = PASTEBIN_CREATING_PASTE_URL
        payload = PASTEBIN_CREATING_PASTE_PAYLOAD.format(
            api_key,
            api_paste_code,
            api_option,
            api_user_key,
            api_paste_name,
            api_paste_format,
            api_paste_exposure,
            api_paste_expiration
        )
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        ret_val, response = self._make_rest_call(
            url=url,
            action_result=action_result,
            headers=headers,
            data=payload,
            timeout=30,
            method="post"
        )
        if phantom.is_fail(ret_val):
            return action_result.get_status(), None

        return action_result.set_status(phantom.APP_SUCCESS, "Link obtained successfully"), response

    def _handle_create_paste(self, param):
        action_result = self.add_action_result(ActionResult(dict(param)))
        try:
            api_paste_code = urllib.parse.quote(param['paste_text'].encode('utf8'))
            api_option = 'paste'

            api_user_key = param.get("paste_as_user", False)
            api_paste_name = param.get("paste_title", "")
            api_paste_format = param.get("paste_format", "")
            api_paste_exposure = param.get("paste_exposure", "")
            api_paste_expiration = param.get("paste_expiration", "")

            if api_user_key or api_paste_exposure == 'Private':
                if not self._pastebin_username or not self._pastebin_password:
                    return action_result.set_status(
                        phantom.APP_ERROR,
                        "Please provide pastebin username and password in asset configuration parameters to create paste as a user"
                    )
                if api_paste_exposure == 'Private' and not api_user_key:
                    return action_result.set_status(
                        phantom.APP_ERROR,
                        """Pasting private as guest is not supported.
                            Please checkbox 'paste as user' parameter in create_paste action to set the exposure of the paste as private"""
                    )
                ret_val, api_user_key = self._get_user_key(
                    action_result,
                    self._pastebin_username,
                    self._pastebin_password
                )
                if phantom.is_fail(ret_val):
                    return action_result.get_status()
            else:
                api_user_key = ""

            if api_paste_format:
                for key in PASTEBIN_FORMAT_DICT:
                    if api_paste_format == key:
                        api_paste_format = PASTEBIN_FORMAT_DICT[key]

            if api_paste_exposure:
                for key in PASTEBIN_PRIVATE_DICT:
                    if api_paste_exposure == key:
                        api_paste_exposure = PASTEBIN_PRIVATE_DICT[key]

            if api_paste_expiration:
                for key in PASTEBIN_EXPIRE_DATE_DICT:
                    if api_paste_expiration == key:
                        api_paste_expiration = PASTEBIN_EXPIRE_DATE_DICT[key]

            ret_val, link = self._creating_paste(
                action_result,
                self._api_key,
                api_paste_code,
                api_option,
                api_user_key,
                api_paste_name,
                api_paste_format,
                api_paste_exposure,
                api_paste_expiration
            )
            if phantom.is_fail(ret_val):
                return action_result.get_status()

            action_result.add_data({"url": link})
            return action_result.set_status(phantom.APP_SUCCESS, "Paste created successfully")

        except Exception as e:
            action_result.set_status(phantom.APP_ERROR, e)
            return action_result.get_status()

    def _handle_get_data(self, param):
        action_result = self.add_action_result(ActionResult(dict(param)))
        container_id = self.get_container_id()

        url = param['paste_url']
        try:
            pasteid = urlparse(url).path.strip('/')
        except Exception as e:
            error_msg = "Unable to get paste id from the URL. Please provide valid 'paste url' parameter. {0}".format(
                self._get_error_message_from_exception(e))
            return action_result.set_status(phantom.APP_ERROR, error_msg)

        try:
            self.save_progress("Fetching paste with ID {0}".format(pasteid))
            ret_val, response = self._make_rest_call(
                url=url,
                action_result=action_result,
                timeout=30,
                method="get"
            )
            if phantom.is_fail(ret_val):
                return action_result.get_status()

            soup = BeautifulSoup(response, 'html.parser')

            if soup.title.string == 'Pastebin.com - Page Removed':
                action_result.add_data({
                    'pasteid': pasteid,
                    'creation_time': "N/A",
                    'author': "N/A",
                    'title': "This page has been removed!",
                    'paste_data': """This page is no longer available. It has either expired,
 been removed by its creator, or removed by one of the Pastebin staff."""
                })
            else:
                paste_title = soup.find("div", class_="info-top").h1.string
                paste_author = soup.find("div", class_="username").a.string if soup.find("div", class_="username").a else 'Guest'
                paste_time = soup.find("div", class_="date").span['title']
                paste_time = self._convert_to_client_tz(paste_time)
                paste_data = soup.find("textarea", class_="textarea -raw js-paste-raw").string

                action_result.add_data({
                    'pasteid': pasteid,
                    'creation_time': paste_time,
                    'author': paste_author,
                    'title': paste_title,
                    'paste_data': paste_data
                })

                self.save_progress("Saving paste to vault...")
                self._add_file_to_vault(action_result, pasteid + '.txt', container_id, paste_data)
            return action_result.set_status(phantom.APP_SUCCESS, "File added to vault successfully")

        except Exception as e:
            action_result.set_status(phantom.APP_ERROR, "Failed to download paste: ", e)
            return action_result.get_status()

    def handle_action(self, param):
        ret_val = phantom.APP_SUCCESS
        actn_req = self.get_action_identifier()
        self.debug_print("action_id", self.get_action_identifier())

        if actn_req == 'get_data':
            ret_val = self._handle_get_data(param)

        elif actn_req == 'create_paste':
            ret_val = self._handle_create_paste(param)

        elif actn_req == 'test_connectivity':
            ret_val = self._handle_test_connectivity(param)

        return ret_val

    def initialize(self):
        # Load the state in initialize, use it to store data
        # that needs to be accessed across actions
        self._state = self.load_state()

        if not isinstance(self._state, dict):
            self.debug_print("Resetting the state file with the default format")
            self._state = {"app_version": self.get_app_json().get("app_version")}

        config = self.get_config()
        self._api_key = config['api_dev_key']
        self._pastebin_username = config.get("pastebin_username", "")
        self._pastebin_password = config.get("pastebin_password", "")

        return phantom.APP_SUCCESS

    def finalize(self):

        # Save the state, this data is saved across actions and app upgrades
        self.save_state(self._state)
        return phantom.APP_SUCCESS


if __name__ == '__main__':

    import sys

    import pudb
    pudb.set_trace()

    if (len(sys.argv) < 2):
        print("No test json specified as input")
        exit(0)

    with open(sys.argv[1]) as f:
        in_json = f.read()
        in_json = json.loads(in_json)
        print((json.dumps(in_json, indent=4)))

        connector = PasteBinConnector()
        connector.print_progress_message = True
        ret_val = connector._handle_action(json.dumps(in_json), None)
        print(json.dumps(json.loads(ret_val), indent=4))

    exit(0)

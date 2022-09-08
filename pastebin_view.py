# File: pastebin_view.py
#
# Copyright (c) 2019-2022 Splunk Inc.
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
def _get_data_result(result):

    ctx_result = {}
    param = result.get_param()
    data = result.get_data()
    status = result.get_status()

    ctx_result['status'] = status
    ctx_result['param'] = param
    if (data):
        ctx_result['data'] = data[0]

    return ctx_result


def display_paste(provides, all_app_runs, context):

    context['results'] = results = []

    for summary, action_results in all_app_runs:
        for result in action_results:
            get_data_result = _get_data_result(result)
            if (get_data_result is None):
                continue
            results.append(get_data_result)

    if provides == 'get data':
        return 'pastebin_display_paste.html'

    if provides == 'create paste':
        return 'pastebin_create_paste.html'

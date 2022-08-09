def _get_data_result(result):

    ctx_result = {}
#    param = result.get_param()
    data = result.get_data()
    status = result.get_status()

    ctx_result['status'] = status
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

    return 'pastebin_display_paste.html'

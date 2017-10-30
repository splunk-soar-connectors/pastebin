def _get_fetch_paste_result(result):

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
            fetch_paste_result = _get_fetch_paste_result(result)
            if (fetch_paste_result is None):
                continue
            results.append(fetch_paste_result)

    return 'display_paste.html'

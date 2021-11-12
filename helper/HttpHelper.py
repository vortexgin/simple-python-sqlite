import re

from flask import request


def get_filter_query():
    filter = {}

    for field in request.args.to_dict():
        match = re.match('filters\[(.*)\]', field)
        if match is not None:
            filter[match.group(1)] = request.args.get(field)

        match = re.match('filters\[(.*)\]\[(.*)\]', field)
        if match is not None:
            filter[match.group(1)][match.group(2)] = request.args.get(field)

    return filter


def parse_multi_form(form):
    data = {}
    for url_k in form:
        v = form[url_k]
        ks = []
        while url_k:
            if '[' in url_k:
                k, r = url_k.split('[', 1)
                ks.append(k)
                if r[0] == ']':
                    ks.append('')
                url_k = r.replace(']', '', 1)
            else:
                ks.append(url_k)
                break
        sub_data = data
        for i, k in enumerate(ks):
            if k.isdigit():
                k = int(k)
            if i + 1 < len(ks):
                if not isinstance(sub_data, dict):
                    break
                if k in sub_data:
                    sub_data = sub_data[k]
                else:
                    sub_data[k] = {}
                    sub_data = sub_data[k]
            else:
                if isinstance(sub_data, dict):
                    sub_data[k] = v
    return data

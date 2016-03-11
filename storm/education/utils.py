from six.moves import urllib

import yurl


def preserve_request_params(request, url):
    url = yurl.URL(url)
    new_query = urllib.parse.parse_qs(url.query)
    query = urllib.parse.parse_qs(yurl.URL(request.get_full_path()).query)
    query.update(new_query)
    query = urllib.parse.urlencode(query, doseq=True)
    return str(url.replace(query=query))

import pycurl
from StringIO import StringIO
import re

def urljoin(parts, params=None):
    url = '/'.join(part.strip('/') for part in parts)
    if not params:
        return url
    url_params = [p[0] + '=' + str(p[1]) for p in params.items()]
    return url + '?' + '&'.join(url_params)

def _get_http_status(status_line):
    m = re.match(r'HTTP\/\S*\s*\d+\s*(.*?)\s*$', status_line)
    return m.groups(1)[0] if m else ''

def http_get(url, accept, auth_token=None):
    request_headers = ['Accept: ' + accept]
    if auth_token:
        request_headers.append('Authorization-Token: ' + auth_token)
    response_body = StringIO()
    header = StringIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.WRITEFUNCTION, response_body.write)
    c.setopt(c.HEADERFUNCTION, header.write)
    if request_headers:
        c.setopt(c.HTTPHEADER, request_headers)
    c.perform()
    status_code = c.getinfo(pycurl.HTTP_CODE)
    c.close()
    status_line = _get_http_status(header.getvalue().splitlines()[0])
    return (status_code, status_line, response_body.getvalue())

def http_post(url, content_type, body, accept, auth_token=None):
    request_headers = ['Content-Type: ' + content_type, 'Accept: ' + accept]
    if auth_token:
        request_headers.append('Authorization-Token: ' + str(auth_token))
    response_body = StringIO()
    header = StringIO()
    c = pycurl.Curl()
    c.setopt(c.POST, 1)
    c.setopt(c.URL, url)
    c.setopt(c.WRITEFUNCTION, response_body.write)
    c.setopt(c.HEADERFUNCTION, header.write)
    c.setopt(c.HTTPHEADER, request_headers)
    c.setopt(c.POSTFIELDS, body)
    c.perform()
    status_code = c.getinfo(pycurl.HTTP_CODE)
    c.close()
    status_line = _get_http_status(header.getvalue().splitlines()[0])
    return (status_code, status_line, response_body.getvalue())

def http_upload_filepath(url, filepath, content_type, alternate_filename = None):
    response_body = StringIO()
    header = StringIO()
    c = pycurl.Curl()
    c.setopt(c.POST, 1)
    c.setopt(c.URL, url)
    c.setopt(c.WRITEFUNCTION, response_body.write)
    c.setopt(c.HEADERFUNCTION, header.write)
    if alternate_filename:
        c.setopt(c.HTTPPOST, [("file", (c.FORM_FILE, filepath, c.FORM_CONTENTTYPE, content_type, c.FORM_FILENAME, alternate_filename))])
    else:
        c.setopt(c.HTTPPOST, [("file", (c.FORM_FILE, filepath, c.FORM_CONTENTTYPE, content_type))])
    c.perform()
    status_code = c.getinfo(pycurl.HTTP_CODE)
    c.close()
    status_line = _get_http_status(header.getvalue().splitlines()[0])
    return (status_code, status_line, response_body.getvalue())

def http_upload_raw_stream(url, stream, content_type, filename, filesize):
    response_body = StringIO()
    header = StringIO()
    c = pycurl.Curl()
    c.setopt(c.POST, 1)
    c.setopt(c.URL, url)
    c.setopt(c.WRITEFUNCTION, response_body.write)
    c.setopt(c.HEADERFUNCTION, header.write)
    c.setopt(c.HTTPHEADER, ['Content-Type: ' + content_type, 'Content-Disposition: attachment; filename="' + filename + '"', 'Content-Length: ' + str(filesize)])
    c.setopt(c.READFUNCTION, stream.read)
    c.perform()
    status_code = c.getinfo(pycurl.HTTP_CODE)
    c.close()
    status_line = _get_http_status(header.getvalue().splitlines()[0])
    return (status_code, status_line, response_body.getvalue())

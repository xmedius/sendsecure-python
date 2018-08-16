import pycurl
from StringIO import StringIO
import re
import os
import platform
import urllib
from urlparse import urlparse, urlunparse


def _get_cacert_path():
    if platform.system().lower() == 'windows':
        #use the package cacert file that contains more recent cacerts
        return os.path.dirname(__file__) + '\\cacert.pem'
    return None

def urljoin(parts, params=None):
    url = '/'.join(part.strip('/') for part in parts)
    if not params:
        return url
    url_params = [p[0] + '=' + str(p[1]) for p in params.items()]

    parsed_url = list(urlparse(url))
    if parsed_url[4]:
        url_params.append(parsed_url[4])
    parsed_url[4] = '&'.join(url_params)
    return urlunparse(parsed_url)

def _get_http_status(status_lines):
    last_status_line = status_lines[0]
    for line in status_lines:
        if line.startswith('HTTP/'):
            last_status_line = line
    m = re.match(r'HTTP\/\S*\s*\d+\s*(.*?)\s*$', last_status_line)
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
    cacert_file = _get_cacert_path()
    if cacert_file:
        c.setopt(c.CAINFO, cacert_file)
    c.perform()
    status_code = c.getinfo(pycurl.HTTP_CODE)
    c.close()
    status_line = _get_http_status(header.getvalue().splitlines())
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
    cacert_file = _get_cacert_path()
    if cacert_file:
        c.setopt(c.CAINFO, cacert_file)
    c.perform()
    status_code = c.getinfo(pycurl.HTTP_CODE)
    c.close()
    status_line = _get_http_status(header.getvalue().splitlines())
    return (status_code, status_line, response_body.getvalue())

def http_patch(url, content_type, body, accept, auth_token=None):
    request_headers = ['Content-Type: ' + content_type, 'Accept: ' + accept]
    if auth_token:
        request_headers.append('Authorization-Token: ' + str(auth_token))
    response_body = StringIO()
    header = StringIO()
    c = pycurl.Curl()
    c.setopt(pycurl.CUSTOMREQUEST, "PATCH")
    c.setopt(c.POST, 1)
    c.setopt(c.URL, url)
    c.setopt(c.WRITEFUNCTION, response_body.write)
    c.setopt(c.HEADERFUNCTION, header.write)
    c.setopt(c.HTTPHEADER, request_headers)
    c.setopt(c.POSTFIELDS, body)
    cacert_file = _get_cacert_path()
    if cacert_file:
        c.setopt(c.CAINFO, cacert_file)
    c.perform()
    status_code = c.getinfo(pycurl.HTTP_CODE)
    c.close()
    status_line = _get_http_status(header.getvalue().splitlines())
    return (status_code, status_line, response_body.getvalue())

def http_delete(url, accept, auth_token=None):
    request_headers = ['Accept: ' + accept]
    if auth_token:
        request_headers.append('Authorization-Token: ' + auth_token)
    response_body = StringIO()
    header = StringIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(pycurl.CUSTOMREQUEST, "DELETE")
    c.setopt(c.WRITEFUNCTION, response_body.write)
    c.setopt(c.HEADERFUNCTION, header.write)
    c.setopt(c.HTTPHEADER, request_headers)
    cacert_file = _get_cacert_path()
    if cacert_file:
        c.setopt(c.CAINFO, cacert_file)
    c.perform()
    status_code = c.getinfo(pycurl.HTTP_CODE)
    c.close()
    status_line = _get_http_status(header.getvalue().splitlines())
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
    cacert_file = _get_cacert_path()
    if cacert_file:
        c.setopt(c.CAINFO, cacert_file)
    c.perform()
    status_code = c.getinfo(pycurl.HTTP_CODE)
    c.close()
    status_line = _get_http_status(header.getvalue().splitlines())
    return (status_code, status_line, response_body.getvalue())

def http_upload_raw_stream(url, stream, content_type, filename, filesize):
    response_body = StringIO()
    header = StringIO()
    c = pycurl.Curl()
    c.setopt(c.POST, 1)
    c.setopt(c.URL, url)
    c.setopt(c.WRITEFUNCTION, response_body.write)
    c.setopt(c.HEADERFUNCTION, header.write)
    if all(ord(c) < 128 for c in filename):
        c.setopt(c.HTTPHEADER, ['Content-Type: ' + content_type, 'Content-Disposition: attachment; filename="' + str(filename) + '"', 'Content-Length: ' + str(filesize)])
    else:
        c.setopt(c.HTTPHEADER, ['Content-Type: ' + content_type, 'Content-Disposition: attachment; filename*=UTF-8\'\'' + urllib.quote_plus(filename.encode('utf-8')), 'Content-Length: ' + str(filesize)])
    c.setopt(c.READFUNCTION, stream.read)
    cacert_file = _get_cacert_path()
    if cacert_file:
        c.setopt(c.CAINFO, cacert_file)
    c.perform()
    status_code = c.getinfo(pycurl.HTTP_CODE)
    c.close()
    status_line = _get_http_status(header.getvalue().splitlines())
    return (status_code, status_line, response_body.getvalue())

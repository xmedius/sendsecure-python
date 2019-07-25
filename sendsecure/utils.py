from io import BytesIO

import sys

import re
import os
import platform
import urllib
import secrets

from urllib import request
from urllib.parse import urlparse, urlunparse

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
        str_line = line.decode('utf-8')
        if str_line.startswith('HTTP/'):
            last_status_line = str_line
    m = re.match(r'HTTP\/\S*\s*\d+\s*(.*?)\s*$', last_status_line)
    return m.groups(1)[0] if m else ''

def _request(url, method, accept, auth_token=None, body=''):
    req = request.Request(url, body.encode('utf8'), method=method)
    req.add_header('Content-type', "application/json")
    req.add_header('Accept', "application/json")
    if auth_token:
        req.add_header('authorization-token', auth_token)
    res = request.urlopen(req);
    content = res.read().decode('utf-8')
    return (res.status, res.reason, content)


def http_get(url, accept="application/json", auth_token=None):
    return _request(url, 'GET', accept, auth_token=auth_token)


def http_post(url, content_type, body, accept="application/json", auth_token=None):
    return _request(url, 'POST', accept, body=body, auth_token=auth_token)


def http_put(url, content_type, body, accept="application/json", auth_token=None):
    return _request(url, 'PUT', accept, body=body, auth_token=auth_token)

def http_patch(url, content_type, body, accept="application/json", auth_token=None):
    return _request(url, 'PATCH', accept, body=body, auth_token=auth_token)

def http_delete(url, accept="application/json", auth_token=None):
    return _request(url, 'DELETE', accept, auth_token=auth_token)

def http_upload_filepath(url, filepath, content_type, alternate_filename = None):
    filename = alternate_filename or os.path.basename(filepath)
    with open(filepath, 'rb') as filestream:
        return http_upload_raw_stream(url, filestream, content_type, filename, 0)

def http_upload_raw_stream(url, stream, content_type, filename, filesize=0):
    try:
        (multipart, body) = make_file_multipart(filename, stream, content_type)

        req = request.Request(url, data=body, method='POST')
        req.add_header('Content-type', multipart)
        res = request.urlopen(req)
        return (res.status, res.reason, res.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        print(e.headers)  # Read the body of the error response
        raise e


def make_file_multipart(filename, handle, content_type, field='file'):
    endl = b'\r\n'

    boundary_value = secrets.token_hex(16)
    boundary = b'--' + boundary_value.encode('utf-8')
    head = get_multipart_content_type(boundary_value)

    body = BytesIO()
    body.write(boundary + endl)
    body.write(get_part_header(field, filename, content_type))
    body.write(handle.read())
    body.write(endl)
    body.write( boundary + b'--' + endl)
    return (head, body.getvalue())

def get_multipart_content_type(boundary_value):
    return 'multipart/form-data; boundary={}'.format(
        boundary_value)

def get_part_header(name, filename, content_type):
    return ('Content-Disposition: form-data; '
            'name="{}"; filename="{}"\r\n'
            'Content-Type: {}\r\n\r\n').format(name, filename, content_type).encode('utf-8')

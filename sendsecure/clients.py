
import json
import os
from .utils import *
from .helpers import *

class SendSecureException(Exception):
    def __init__(self, code, message, details):
        self.code = code
        self.message = message
        self.details = details
    def __str__(self):
        return str(self.code) + ': ' + self.message

class UnexpectedServerResponseException(SendSecureException):
    def __init__(self, code, message, details):
        SendSecureException.__init__(self, code, message, details)

class JsonClient:
    def __init__(self, api_token, enterprise_account, endpoint='https://portal.xmedius.com', locale='en'):
        self.locale = locale
        self.enterprise_account = enterprise_account
        self.endpoint = endpoint
        self.sendsecure_endpoint = None
        self.api_token = str(api_token)

    def new_safebox(self, user_email):
        params = {'user_email' : user_email, 'locale' : self.locale}
        url = urljoin([self._get_sendsecure_endpoint(), 'api/v2/safeboxes/new'], params)
        return self._do_get(url, 'application/json')

    def upload_file(self, upload_url, source, content_type='application/octet-stream', filename=None, filesize=None):
        status_code = None
        status_line = None
        response_body = None
        if type(source) == str:
            (status_code, status_line, response_body) = http_upload_filepath(str(upload_url), source, content_type, filename)
        elif type(source) == file:
            upload_filename = filename or source.name.split('/')[-1]
            upload_filesize = filesize or (os.path.getsize(source.name) - source.tell())
            (status_code, status_line, response_body) = http_upload_raw_stream(str(upload_url), source, content_type, upload_filename, upload_filesize)
        else:
            (status_code, status_line, response_body) = http_upload_raw_stream(str(upload_url), source, content_type, filename, filesize)
        if status_code >= 400:
            raise SendSecureException(status_code, status_line, response_body)
        return response_body

    def commit_safebox(self, safebox_json):
        params = {'locale' : self.locale}
        url = urljoin([self._get_sendsecure_endpoint(), 'api/v2/safeboxes'], params)
        return self._do_post(url, 'application/json', safebox_json, 'application/json')

    def get_security_profiles(self, user_email):
        params = {'user_email' : user_email, 'locale' : self.locale}
        url = urljoin([self._get_sendsecure_endpoint(), 'api/v2/enterprises', self.enterprise_account, 'security_profiles'], params)
        return self._do_get(url, 'application/json')

    def get_enterprise_settings(self):
        params = {'locale' : self.locale}
        url = urljoin([self._get_sendsecure_endpoint(), 'api/v2/enterprises', self.enterprise_account, 'settings'], params)
        return self._do_get(url, 'application/json')

    def _get_sendsecure_endpoint(self):
        if not self.sendsecure_endpoint:
            url = urljoin([self.endpoint, 'services', self.enterprise_account, 'sendsecure/server/url'])
            self.sendsecure_endpoint = self._do_get(url, 'text/plain')
        return self.sendsecure_endpoint

    def _do_get(self, url, accept):
        (status_code, status_line, response_body) = http_get(url, accept, self.api_token)
        if status_code >= 400:
            raise SendSecureException(status_code, status_line, response_body)
        return response_body

    def _do_post(self, url, content_type, body, accept):
        (status_code, status_line, response_body) = http_post(url, content_type, body, accept, self.api_token)
        if status_code >= 400:
            raise SendSecureException(status_code, status_line, response_body)
        return response_body


class Client:
    @staticmethod
    def get_user_token(enterprise_account, username, password, device_id, device_name,
        application_type='SendSecure Python', endpoint='https://portal.xmedius.com', one_time_password=''):
        url = urljoin([endpoint, 'services', enterprise_account, 'portal/host'])
        (status_code, status_line, response_body) = http_get(url, 'text/plain')
        if status_code >= 400:
            raise SendSecureException(status_code, status_line, response_body)

        url = urljoin([response_body, 'api/user_token'])
        post_params = {
            'permalink': enterprise_account,
            'username': username,
            'password': password,
            'application_type': application_type,
            'device_id': device_id,
            'device_name': device_name,
            'otp': one_time_password
        }
        (status_code, status_line, response_body) = http_post(url, 'application/json', json.dumps(post_params), 'application/json')
        if status_code >= 400:
            error_code = status_code
            error_message = status_line
            try:
                j = json.loads(response_body)
                error_code = j['code']
                error_message = j['message']
            except:
                pass
            raise SendSecureException(error_code, error_message, response_body)

        try:
            j = json.loads(response_body)
            return j['token']
        except:
            raise UnexpectedServerResponseException(500, 'Unexpected Error', '')

    def __init__(self, api_token, enterprise_account, endpoint='https://portal.xmedius.com', locale='en'):
        self.json_client = JsonClient(api_token, enterprise_account, endpoint, locale)

    def get_enterprise_settings(self):
        result = self.json_client.get_enterprise_settings()
        return EnterpriseSettings.from_json(result)

    def get_security_profiles(self, user_email):
        result = self.json_client.get_security_profiles(user_email)
        security_profiles = []
        j = json.loads(result)
        for elem in j['security_profiles']:
            security_profiles.append(SecurityProfile.from_json(json.dumps(elem)))
        return security_profiles

    def get_default_security_profile(self, user_email):
        enterprise_settings = self.get_enterprise_settings()
        security_profiles = self.get_security_profiles(user_email)
        for p in security_profiles:
            if p.id == enterprise_settings.default_security_profile_id:
                return p
        return None

    def initialize_safebox(self, safebox):
        result = self.json_client.new_safebox(safebox.user_email)
        j = json.loads(result)
        safebox.guid = j['guid']
        safebox.public_encryption_key = j['public_encryption_key']
        safebox.upload_url = j['upload_url']

    def upload_attachment(self, safebox, attachment):
        result = self.json_client.upload_file(safebox.upload_url,
            attachment.source, attachment.content_type, attachment.filename, attachment.size)
        j = json.loads(result)
        attachment.guid = j['temporary_document']['document_guid']
        return attachment

    def commit_safebox(self, safebox):
        result = self.json_client.commit_safebox(safebox.to_json())
        return SafeboxResponse.from_json(result)

    def submit_safebox(self, safebox):
        self.initialize_safebox(safebox)
        for attachment in safebox.attachments:
            self.upload_attachment(safebox, attachment)
        if not safebox.security_profile:
            safebox.security_profile = self.get_default_security_profile(safebox.user_email)
        return self.commit_safebox(safebox)

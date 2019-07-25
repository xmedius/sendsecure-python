import os
import io
from .utils import *
from .exceptions import *


class JsonClient:
    """
    JsonClient object constructor.

    @param api_token:
               The API Token to be used for authentication with the SendSecure service
    @param user_id:
               The user id of the current user
    @param enterprise_account:
               The SendSecure enterprise account
    @param endpoint:
               The URL to the SendSecure service ("https://portal.xmedius.com" will be used by default if empty)
    @param locale:
               The locale in which the server errors will be returned ("en" will be used by default if empty)
    """
    def __init__(self, options):
        self.locale = options.get('locale', 'en')
        self.enterprise_account = options.get('enterprise_account')
        self.endpoint = options.get('endpoint', 'https://portal.xmedius.com')
        self.sendsecure_endpoint = None
        self.token = str(options.get('token'))
        self.user_id = options.get('user_id')

    """
    Pre-creates a SafeBox on the SendSecure system and initializes the Safebox object accordingly.

    @param user_email:
              The email address of a SendSecure user of the current enterprise account
    @return: The json containing the guid, public encryption key and upload url of the initialize SafeBox
    """
    def new_safebox(self, user_email):
        params = {'user_email': user_email}
        url = urljoin([self._get_sendsecure_endpoint(), 'api/v2/safeboxes/new.json'], params)
        return self._do_get(url, 'application/json')

    """
    Pre-creates a document on the SendSecure system and initializes the Safebox object accordingly.

    @param safebox_guid:
                The guid of the existing safebox
    @param file_params:
                The full json expected by the server
    @return: The json containing the temporary document GUID and the upload URL
    """
    def new_file(self, safebox_guid, file_params):
        url = urljoin([self._get_sendsecure_endpoint(), 'api/v2/safeboxes/', safebox_guid, 'uploads.json'])
        return self._do_post(url, 'application/json', file_params, 'application/json')

    """
    Uploads the specified file as an Attachment of the specified SafeBox.

    @param upload_url:
                The url returned by the initializeSafeBox. Can be used multiple time
    @param source:
                The path of the file to upload or the stream
    @param content_type:
                The MIME content type of the uploaded file
    @param filename:
                The file name
    @param filesize:
                The filesize
    @return: The json containing the guid of the uploaded file
    """
    def upload_file(self, upload_url, source, content_type='application/octet-stream', filename=None, filesize=None):
        status_code = None
        status_line = None
        response_body = None
        if type(source) == str:
            (status_code, status_line, response_body) = http_upload_filepath(str(upload_url), source, content_type, filename)
        elif self._is_file(source):
            upload_filename = filename or source.name.split('/')[-1]
            upload_filesize = filesize or (os.path.getsize(source.name) - source.tell())
            (status_code, status_line, response_body) = http_upload_raw_stream(str(upload_url), source, content_type, upload_filename, upload_filesize)
        else:
            (status_code, status_line, response_body) = http_upload_raw_stream(str(upload_url), source, content_type, filename, filesize)
        if status_code >= 400:
            raise SendSecureException(status_code, status_line, response_body)
        return response_body

    """
    Finalizes the creation (commit) of the SafeBox on the SendSecure system. This actually "Sends" the SafeBox with
    all content and contact info previously specified.

    @param safebox_json:
                The full json expected by the server
    @return: The json containing the guid, preview url and encryption key of the created SafeBox
    """
    def commit_safebox(self, safebox_json):
        url = urljoin([self._get_sendsecure_endpoint(), 'api/v2/safeboxes.json'])
        return self._do_post(url, 'application/json', safebox_json, 'application/json')

    """
    Retrieves all available security profiles of the enterprise account for a specific user.

    @param user_email:
                The email address of a SendSecure user of the current enterprise account
    @return: The json containing a list of Security Profiles
    """
    def get_security_profiles(self, user_email):
        params = {'user_email': user_email}
        url = urljoin([self._get_sendsecure_endpoint(), 'api/v2/enterprises', self.enterprise_account, 'security_profiles.json'], params)
        return self._do_get(url, 'application/json')

    """
    Get the Enterprise Settings of the current enterprise account.

    @return: The json containing the enterprise settings
    """
    def get_enterprise_settings(self):
        url = urljoin([self._get_sendsecure_endpoint(), 'api/v2/enterprises', self.enterprise_account, 'settings.json'])
        return self._do_get(url, 'application/json')

    """
    Get the User Settings of the current user account

    @return: The json containing the user settings
    """
    def get_user_settings(self):
        url = urljoin([self._get_sendsecure_endpoint(), 'api/v2/enterprises', self.enterprise_account, 'users', self.user_id, 'settings.json'])
        return self._do_get(url, 'application/json')

    """
    Retrieves all favorites for the current user account.

    @return: The json containing a list of Favorite
    """
    def get_favorites(self):
        url = urljoin([self._get_sendsecure_endpoint(), 'api/v2/enterprises', self.enterprise_account, 'users', self.user_id, 'favorites.json'])
        return self._do_get(url, 'application/json')

    """
    Create a new favorite for the current user account.

    @param favorite_json:
                The full json expected by the server
    @return: The json containing all the informations of the created Favorite
    """
    def create_favorite(self, favorite_json):
        url = urljoin([self._get_sendsecure_endpoint(), 'api/v2/enterprises', self.enterprise_account, 'users', self.user_id, 'favorites.json'])
        return self._do_post(url, 'application/json', favorite_json, 'application/json')

    """
    Update an existing favorite for the current user account.

    @param favorite_id
                The id of the favorite to be updated
    @param favorite_params
                The full json expected by the server

    @return: The json containing all the informations of the updated Favorite
    """
    def update_favorite(self, favorite_id, favorite_json):
        url = urljoin([self._get_sendsecure_endpoint(), 'api/v2/enterprises', self.enterprise_account, 'users', self.user_id, 'favorites', str(favorite_id) + '.json'])
        return self._do_patch(url, 'application/json', favorite_json, 'application/json')

    """
    Delete an existing favorite for the current user account.

    @param favorite_id:
                   The id of the Favorite to be deleted
    @return: Nothing
    """
    def delete_favorite(self, favorite_id):
        url = urljoin([self._get_sendsecure_endpoint(), 'api/v2/enterprises', self.enterprise_account, 'users', self.user_id, 'favorites', str(favorite_id) + '.json'])
        return self._do_delete(url, 'application/json')

    """
    Create a new participant for a specific open safebox of the current user account.

    @param safebox_guid:
                The guid of the safebox to be updated
    @param participant_json:
                The full json expected by the server
    @return: The json containing all the informations of the created Participant
    """
    def create_participant(self, safebox_guid, participant_json):
        url = urljoin([self._get_sendsecure_endpoint(), 'api/v2/safeboxes', safebox_guid, 'participants.json'])
        return self._do_post(url, 'application/json', participant_json, 'application/json')

    """
    Update an existing participant for a specific open safebox of the current user account.

    @param safebox_guid:
                The guid of the safebox to be updated
    @param participant_id:
                The id of the participant to be updated
    @param participant_json
                The full json expected by the server

    @return: The json containing all the informations of the updated Participant
    """
    def update_participant(self, safebox_guid, participant_id, participant_json):
        url = urljoin([self._get_sendsecure_endpoint(), 'api/v2/safeboxes', safebox_guid, 'participants', participant_id + '.json'])
        return self._do_patch(url, 'application/json', participant_json, 'application/json')

    """
    Search the recipients for a safebox

    @param term:
            A Search term

    @return: The json containing the search result
    """
    def search_recipient(self, term):
        url = urljoin([self._get_sendsecure_endpoint(), 'api/v2/recipients/autocomplete?term=' + term])
        return self._do_get(url, 'application/json')

    """
    Reply to a specific safebox associated to the current user's account.

    @param safebox_guid:
                The guid of the safebox to be updated
    @param reply_params:
                The full json expected by the server

    @return: The json containing the request result
    """
    def reply(self, safebox_guid, reply_params):
        url = urljoin([self._get_sendsecure_endpoint(), 'api/v2/safeboxes', safebox_guid, '/messages.json'])
        return self._do_post(url, 'application/json', reply_params, 'application/json')

    """
    Manually add time to expiration date for a specific open safebox of the current user account.

    @param safebox_guid:
                The guid of the safebox to be updated
    @param add_time_json:
                The full json expected by the server
    @return: The json containing the new expiration date
    """
    def add_time(self, safebox_guid, add_time_json):
        url = urljoin([self._get_sendsecure_endpoint(), 'api/v2/safeboxes', safebox_guid, 'add_time.json'])
        return self._do_patch(url, 'application/json', add_time_json, 'application/json')

    """
    Manually close an existing safebox for the current user account.

    @param safebox_guid:
                The guid of the safebox to be closed
    @return: The json containing the request result
    """
    def close_safebox(self, safebox_guid):
        url = urljoin([self._get_sendsecure_endpoint(), 'api/v2/safeboxes', safebox_guid, 'close.json'])
        return self._do_patch(url, 'application/json', '', 'application/json')

    """
    Manually delete the content of a closed safebox for the current user account.

    @param safebox_guid:
                The guid of the safebox
    @return: The json containing the request result
    """
    def delete_safebox_content(self, safebox_guid):
        url = urljoin([self._get_sendsecure_endpoint(), 'api/v2/safeboxes', safebox_guid, 'delete_content.json'])
        return self._do_patch(url, 'application/json', '', 'application/json')

    """
    Manually mark as read an existing safebox for the current user account.

    @param safebox_guid:
                The guid of the safebox
    @return: The json containing the request result
    """
    def mark_as_read(self, safebox_guid):
        url = urljoin([self._get_sendsecure_endpoint(), 'api/v2/safeboxes', safebox_guid, 'mark_as_read.json'])
        return self._do_patch(url, 'application/json', '', 'application/json')

    """
    Manually mark as unread an existing safebox for the current user account.

    @param safebox_guid:
                The guid of the safebox
    @return: The json containing the request result
    """
    def mark_as_unread(self, safebox_guid):
        url = urljoin([self._get_sendsecure_endpoint(), 'api/v2/safeboxes', safebox_guid, 'mark_as_unread.json'])
        return self._do_patch(url, 'application/json', '', 'application/json')

    """
    Manually mark as read an existing message.

    @param safebox_guid:
                The guid of the safebox
    @param message_id:
                The id of the message to be marked as read
    @return: The json containing the request result
    """
    def mark_as_read_message(self, safebox_guid, message_id):
        url = urljoin([self._get_sendsecure_endpoint(), 'api/v2/safeboxes', safebox_guid, 'messages', str(message_id), 'read'])
        return self._do_patch(url, 'application/json', '', 'application/json')

    """
    Manually mark as unread an existing message.

    @param safebox_guid:
                The guid of the safebox
    @param message_id:
                The id of the message to be marked as unread
    @return: The json containing the request result
    """
    def mark_as_unread_message(self, safebox_guid, message_id):
        url = urljoin([self._get_sendsecure_endpoint(), 'api/v2/safeboxes', safebox_guid, 'messages', str(message_id), 'unread'])
        return self._do_patch(url, 'application/json', '', 'application/json')

    """
    Retrieve a specific file url of an existing safebox for the current user account.

    @param safebox_guid:
                The guid of the safebox
    @param document_guid:
                The guid of the file
    @param user_email:
                The current user email

    @return: The json containing the file url on the fileserver
    """
    def get_file_url(self, safebox_guid, document_guid, user_email):
        params = {'user_email': user_email}
        url = urljoin([self._get_sendsecure_endpoint(), 'api/v2/safeboxes', safebox_guid, 'documents', document_guid, 'url.json'], params)
        return self._do_get(url, 'application/json')

    """
    Retrieve the url of the audit record of an existing safebox for the current user account.

    @param safebox_guid:
                The guid of the safebox
    @return: The json containing the url
    """
    def get_audit_record_url(self, safebox_guid):
        url = urljoin([self._get_sendsecure_endpoint(), 'api/v2/safeboxes', safebox_guid, 'audit_record_pdf.json'])
        return self._do_get(url, 'application/json')

    """
    Retrieve the audit record of an existing safebox for the current user account.

    @param url:
            The url of the safebox audit record
    @return: The pdf stream
    """
    def get_audit_record_pdf(self, url):
        return self._get(url, 'application/pdf')

    """
    Retrieve a filtered list of safeboxes for the current user account.

    @param url:
            The complete search url
    @param search_params:
           The optional filtering parameters

    @return: The json containing the count, previous page url, the next page url and a list of Safebox
    """
    def get_safeboxes(self, url, search_params):
        if url is None:
            url = urljoin([self._get_sendsecure_endpoint(), 'api/v2/safeboxes.json'], search_params)
        return self._do_get(url, 'application/json')

    """
    Retrieve all info of an existing safebox for the current user account.

    @param safebox_guid:
               The guid of the safebox to be updated
    @param sections:
               The string containing the list of sections to be retrieved
    @return: The json containing all the informations on the specified sections.
             If no sections are specified, it will return all safebox infos.
    """
    def get_safebox_info(self, safebox_guid, sections):
        params = ''
        if sections:
            params = {'sections': sections}
        url = urljoin([self._get_sendsecure_endpoint(), 'api/v2/safeboxes', safebox_guid + '.json'], params)
        return self._do_get(url, 'application/json')

    """
    Retrieve all participants info of an existing safebox for the current user account.

    @param safebox_guid:
               The guid of the safebox
    @return: The json containing the list of participants
    """
    def get_safebox_participants(self, safebox_guid):
        url = urljoin([self._get_sendsecure_endpoint(), 'api/v2/safeboxes', safebox_guid, 'participants.json'])
        return self._do_get(url, 'application/json')

    """
    Retrieve all messages info of an existing safebox for the current user account.

    @param safebox_guid:
               The guid of the safebox
    @return: The json containing the list of messages
    """
    def get_safebox_messages(self, safebox_guid):
        url = urljoin([self._get_sendsecure_endpoint(), 'api/v2/safeboxes', safebox_guid, 'messages.json'])
        return self._do_get(url, 'application/json')

    """
    Retrieve all security options info of an existing safebox for the current user account.

    @param safebox_guid:
               The guid of the safebox
    @return: The json containing the Security Options
    """
    def get_safebox_security_options(self, safebox_guid):
        url = urljoin([self._get_sendsecure_endpoint(), 'api/v2/safeboxes', safebox_guid, 'security_options.json'])
        return self._do_get(url, 'application/json')

    """
    Retrieve all download activity info of an existing safebox for the current user account.

    @param safebox_guid:
               The guid of the safebox
    @return: The json containing the Download Activity
    """
    def get_safebox_download_activity(self, safebox_guid):
        url = urljoin([self._get_sendsecure_endpoint(), 'api/v2/safeboxes', safebox_guid, 'download_activity.json'])
        return self._do_get(url, 'application/json')

    """
    Retrieve all event_history info of an existing safebox for the current user account.

    @param safebox_guid:
               The guid of the safebox

    @return: The json containing a list of EventHistory
    """
    def get_safebox_event_history(self, safebox_guid):
        url = urljoin([self._get_sendsecure_endpoint(), 'api/v2/safeboxes', safebox_guid, 'event_history.json'])
        return self._do_get(url, 'application/json')

    """
    Archive a specific safebox

    @param safebox_guid:
                The guid of the safebox
    @param user_email:
                The current user email
    @return: The json containing the request result
    """
    def archive_safebox(self, safebox_guid, user_email):
        url = urljoin([self._get_sendsecure_endpoint(), 'api/v2/safeboxes', safebox_guid, '/tag/archive'])
        return self._do_post(url, 'application/json', user_email, 'application/json')

    """
    Remove the tag "archive" from the safebox

    @param safebox_guid:
                The guid of the safebox
    @param user_email:
                The current user email
    @return: The json containing the request result
    """
    def unarchive_safebox(self, safebox_guid, user_email):
        url = urljoin([self._get_sendsecure_endpoint(), 'api/v2/safeboxes', safebox_guid, '/untag/archive'])
        return self._do_post(url, 'application/json', user_email, 'application/json')


    """
    Call to unfollow the SafeBox. By default, all new Safeboxes are "followed"

    @param safebox:
                A Safebox object
    @return: An object containing the request result
    """
    def unfollow(self, safebox_guid):
        url = urljoin([self._get_sendsecure_endpoint(), 'api/v2/safeboxes', safebox_guid, '/unfollow'])
        return self._do_patch(url, 'application/json', '', 'application/json')

    """
    Call to follow the SafeBox (opposite of the unfollow call).

    @param safebox:
                A Safebox object
    @return: An object containing the request result
    """
    def follow(self, safebox_guid):
        url = urljoin([self._get_sendsecure_endpoint(), 'api/v2/safeboxes', safebox_guid, '/follow'])
        return self._do_patch(url, 'application/json', '', 'application/json')


    """
    Call to get the list of all the localized messages of a consent group.

    @param consent_group_id:
                      The id of the consent group
    @return: The json containing the list of all the localized messages
    """
    def get_consent_group_messages(self, consent_group_id):
        url = urljoin([self._get_sendsecure_endpoint(), 'api/v2/enterprises', self.enterprise_account, '/consent_message_groups', str(consent_group_id)])
        return self._do_get(url, 'application/json')

    def _get_sendsecure_endpoint(self):
        if not self.sendsecure_endpoint:
            url = urljoin([self.endpoint, 'services', self.enterprise_account, 'sendsecure/server/url'])
            new_endpoint = self._get(url, 'text/plain')
            self.sendsecure_endpoint = new_endpoint
        return self.sendsecure_endpoint

    def _do_get(self, url, accept):
        params = {'locale': self.locale}
        new_url = urljoin([url], params)
        return self._get(new_url, accept)

    def _get(self, url, accept):
        (status_code, status_line, response_body) = http_get(url, accept, self.token)
        if status_code >= 400:
            raise SendSecureException(status_code, status_line, response_body)
        return response_body

    def _do_post(self, url, content_type, body, accept):
        params = {'locale': self.locale}
        (status_code, status_line, response_body) = http_post(urljoin([url], params), content_type, body, accept, self.token)
        if status_code >= 400:
            raise SendSecureException(status_code, status_line, response_body)
        return response_body

    def _do_patch(self, url, content_type, body, accept):
        params = {'locale': self.locale}
        (status_code, status_line, response_body) = http_patch(urljoin([url], params), content_type, body, accept, self.token)
        if status_code >= 400:
            raise SendSecureException(status_code, status_line, response_body)
        return response_body

    def _do_delete(self, url, accept):
        params = {'locale': self.locale}
        (status_code, status_line, response_body) = http_delete(urljoin([url], params), accept, self.token)
        if status_code >= 400:
            raise SendSecureException(status_code, status_line, response_body)
        return response_body

    def _is_file(self, obj): 
        return isinstance(obj, (io.TextIOBase, io.BufferedIOBase, io.RawIOBase, io.IOBase))
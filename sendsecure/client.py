import json
from utils import *
from helpers import *
from exceptions import *
from json_client import *


class Client:
    """
    Gets an API Token for a specific user within a SendSecure enterprise account.

    @param enterprise_account:
            The SendSecure enterprise account
    @param username:
            The username of a SendSecure user of the current enterprise account
    @param password:
            The password of this user
    @param device_id:
            The unique ID of the device used to get the Token
    @param device_name:
            The name of the device used to get the Token
    @param application_type:
            The type/name of the application used to get the Token ("SendSecure Python" will be used by default if empty)
    @param otp:
            The one-time password of this user (if any)
    @param endpoint:
            The URL to the SendSecure service ("https://portal.xmedius.com" will be used by default if empty)
    @return: (API Token, user ID) to be used for the specified user
    """
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
            return json.loads(response_body)
        except:
            raise UnexpectedServerResponseException(500, 'Unexpected Error', '')

    """
    Client object constructor.

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
        self.json_client = JsonClient(options)

    """
    Retrieves all the current enterprise account's settings specific to a SendSecure Account

    @return: All values/properties of the enterprise account's settings specific to SendSecure.
    """
    def get_enterprise_settings(self):
        result = self.json_client.get_enterprise_settings()
        return EnterpriseSettings(result)

    """
    Retrieves all available security profiles of the enterprise account for a specific user.

    @param user_email:
                The email address of a SendSecure user of the current enterprise account
    @return: The list of all security profiles of the enterprise account, with all their setting values/properties.
    """
    def get_security_profiles(self, user_email):
        result = self.json_client.get_security_profiles(user_email)
        j = json.loads(result)
        return [SecurityProfile(elem) for elem in j['security_profiles']]

    """
    Retrieves the default security profile of the enterprise account for a specific user.
    A default security profile must have been set in the enterprise account, otherwise
    the method will return nothing.

    @param user_email:
                The email address of a SendSecure user of the current enterprise account
    @return: Default security profile of the enterprise, with all its setting values/properties.
    """
    def get_default_security_profile(self, user_email):
        enterprise_settings = self.get_enterprise_settings()
        security_profiles = self.get_security_profiles(user_email)
        for p in security_profiles:
            if p.id == enterprise_settings.default_security_profile_id:
                return p
        return None

    """
    Pre-creates a SafeBox on the SendSecure system and initializes the Safebox object accordingly.

    @param safebox:
              A SafeBox object to be finalized by the SendSecure system
    @return: The updated SafeBox object with the necessary system parameters (GUID, public encryption key, upload URL)
    filled out. Raise SendSecureException if the safebox is already initialize.
    """
    def initialize_safebox(self, safebox):
        result = self.json_client.new_safebox(safebox.user_email)
        return safebox.update_attributes(result)

    """
    Uploads the specified file as an Attachment of the specified SafeBox.

    @param safebox:
                An initialized Safebox object
    @param attachment:
                An Attachment object - the file to upload to the SendSecure system
    @return: The updated Attachment object with the GUID parameter filled out.
    """
    def upload_attachment(self, safebox, attachment):
        result = self.json_client.upload_file(safebox.upload_url,
            attachment.source, attachment.content_type, attachment.filename, attachment.size)
        j = json.loads(result)
        attachment.guid = j['temporary_document']['document_guid']
        return attachment

    """
    This actually "Sends" the SafeBox with all content and contact info previously specified.

    @param safebox:
             A Safebox object already finalized, with security profile, recipient(s),
             subject and message already defined, and attachments already uploaded.
    @return: Updated Safebox
    """
    def commit_safebox(self, safebox):
        if safebox.guid is None:
            raise SendSecureException(0, 'SafeBox GUID cannot be null', '')
        if not safebox.participants:
            raise SendSecureException(0, 'Participants cannot be empty', '')
        if safebox.security_profile_id is None:
            raise SendSecureException(0, 'No Security Profile configured', '')
        json_result = self.json_client.commit_safebox(safebox.to_json())
        result = json.loads(json_result)
        result['is_creation'] = True
        return safebox.update_attributes(result)

    """
    This method is a high-level combo that initializes the SafeBox, uploads all attachments and commits the SafeBox.

    @param safebox:
                A non-initialized Safebox object with security profile, recipient(s), subject,
                message and attachments (not yet uploaded) already defined.
    @return: Updated Safebox
    """
    def submit_safebox(self, safebox):
        self.initialize_safebox(safebox)
        for attachment in safebox.attachments:
            self.upload_attachment(safebox, attachment)
        if safebox.security_profile_id is None:
            safebox.security_profile_id = self.get_default_security_profile(safebox.user_email).id
        return self.commit_safebox(safebox)

    """
    Retrieves all the current user account's settings specific to SendSecure Account

    @return: All values/properties of the user account's settings specific to SendSecure.
    """
    def get_user_settings(self):
        result = self.json_client.get_user_settings()
        return UserSettings(result)

    """
    Retrieves all favorites associated to a specific user.

    @return: The list of all favorites of the user account, with all their properties.
    """
    def get_favorites(self):
        json_result = self.json_client.get_favorites()
        result = json.loads(json_result)
        return [Favorite(params=favorite_params) for favorite_params in result['favorites']]

    """
    Create a new favorite associated to a specific user.

    @param favorite:
                 A Favorite object
    @return: The updated Favorite
    """
    def create_favorite(self, favorite):
        if favorite.email is None:
            raise SendSecureException(0, 'Favorite email cannot be null', '')
        result = self.json_client.create_favorite(favorite.to_json())
        return favorite.update_attributes(result)

    """
    Update an existing favorite associated to a specific user.

    @param favorite:
                 A Favorite object
    @return: The updated Favorite
    """
    def update_favorite(self, favorite):
        if favorite.id is None:
            raise SendSecureException(0, 'Favorite id cannot be null', '')
        result = self.json_client.update_favorite(favorite.id, favorite.to_json())
        return favorite.update_attributes(result)

    """
    Delete contact methods of an existing favorite associated to a specific user.

    @param favorite:
                 A Favorite object
    @param contact_method_ids:
                 An array of contact methods ids
    @return: The updated Favorite
    """
    def delete_favorite_contact_methods(self, favorite, contact_method_ids):
        if favorite.id is None:
            raise SendSecureException(0, 'Favorite id cannot be null', '')
        favorite.prepare_to_destroy_contact(contact_method_ids)
        result = self.json_client.update_favorite(favorite.id, favorite.to_json())
        return favorite.update_attributes(result)

    """
    Delete an existing favorite associated to a specific user.

    @param favorite:
                The favorite to be deleted
    @return: Nothing
    """
    def delete_favorite(self, favorite):
        self.json_client.delete_favorite(favorite.id)

    """
    Create a new participant for a specific safebox associated to the current user's account,
    and add the new participant to the Safebox object.

    @param safebox:
                A Safebox object
    @param participant:
                A Participant object
    @return: The updated Participant
    """
    def create_participant(self, safebox, participant):
        if safebox.guid is None:
            raise SendSecureException(0, 'SafeBox GUID cannot be null', '')
        if participant.email is None:
            raise SendSecureException(0, 'Participant email cannot be null', '')
        result = self.json_client.create_participant(safebox.guid, participant.to_json())
        participant.update_attributes(result)
        safebox.participants.append(participant)
        return participant

    """
    Update an existing participant of a specific safebox associated to the current user's account.

    @param safebox:
                A Safebox object
    @param participant:
                A Participant object
    @return: The updated Participant
    """
    def update_participant(self, safebox, participant):
        if safebox.guid is None:
            raise SendSecureException(0, 'SafeBox GUID cannot be null', '')
        if participant.id is None:
            raise SendSecureException(0, 'Participant id cannot be null', '')
        result = self.json_client.update_participant(safebox.guid, participant.id, participant.to_json())
        return participant.update_attributes(result)

    """
    Delete contact methods of an existing participant of a specific safebox associated to the current user's account.

    @param safebox:
                A Safebox object
    @param participant:
                A Participant object
    @param contact_method_ids:
                An array of contact method id
    @return: The updated Participant
    """
    def delete_participant_contact_methods(self, safebox, participant, contact_method_ids):
        if safebox.guid is None:
            raise SendSecureException(0, 'SafeBox GUID cannot be null', '')
        if participant.id is None:
            raise SendSecureException(0, 'Participant id cannot be null', '')
        participant.prepare_to_destroy_contact(contact_method_ids)
        result = self.json_client.update_participant(safebox.guid, participant.id, participant.to_json())
        return participant.update_attributes(result)

    """
    Search the recipients for a SafeBox

    @param term:
             A Search term
    @return: The list of recipients that matches the search term
    """
    def search_recipient(self, term):
        return json.loads(self.json_client.search_recipient(term))

    """
    Reply to a specific safebox associated to the current user's account.

    @param safebox:
                A Safebox object
    @param reply:
                A reply object
    @return: An object containing the request result
    """
    def reply(self, safebox, reply):
        if safebox.guid is None:
            raise SendSecureException(0, 'SafeBox GUID cannot be null', '')
        for attachment in reply.attachments:
            file_params = safebox._temporary_document(os.path.getsize(attachment.source))
            temporary_file = json.loads(self.json_client.new_file(safebox.guid, json.dumps(file_params)))
            uploaded_file = json.loads(self.json_client.upload_file(temporary_file['upload_url'], attachment.source,
                attachment.content_type, attachment.filename, attachment.size))
            reply.document_ids.append(uploaded_file['temporary_document']['document_guid'])
        result = self.json_client.reply(safebox.guid, reply.to_json())
        return json.loads(result)

    """
    Add time to the expiration date of a specific safebox associated to the current user's account.

    @param safebox:
                A Safebox object
    @param value:
                Time value to be added to the expiration date
    @param unit:
                Time unit to be added to the expiration date
    @return: An object containing the request result
    """
    def add_time(self, safebox, value, unit):
        if safebox.guid is None:
            raise SendSecureException(0, 'SafeBox GUID cannot be null', '')
        add_time_params = { 'safebox': { 'add_time_value': value, 'add_time_unit': unit }}
        result = self.json_client.add_time(safebox.guid, json.dumps(add_time_params))
        return json.loads(result)

    """
    Close a specific safebox associated to the current user's account.

    @param safebox:
                A Safebox object
    @return: An object containing the request result
    """
    def close_safebox(self, safebox):
        if safebox.guid is None:
            raise SendSecureException(0, 'SafeBox GUID cannot be null', '')
        result = self.json_client.close_safebox(safebox.guid)
        return json.loads(result)

    """
    Delete content of a specific safebox associated to the current user's account.

    @param safebox:
                A Safebox object
    @return: An object containing the request result
    """
    def delete_safebox_content(self, safebox):
        if safebox.guid is None:
            raise SendSecureException(0, 'SafeBox GUID cannot be null', '')
        result = self.json_client.delete_safebox_content(safebox.guid)
        return json.loads(result)

    """
    Mark all messages as read of a specific safebox associated to the current user's account.

    @param safebox:
                A Safebox object
    @return: An object containing the request result
    """
    def mark_as_read(self, safebox):
        if safebox.guid is None:
            raise SendSecureException(0, 'SafeBox GUID cannot be null', '')
        result = self.json_client.mark_as_read(safebox.guid)
        return json.loads(result)

    """
    Mark all messages as unread of a specific safebox associated to the current user's account.

    @param safebox:
                A Safebox object
    @return: An object containing the request result
    """
    def mark_as_unread(self, safebox):
        if safebox.guid is None:
            raise SendSecureException(0, 'SafeBox GUID cannot be null', '')
        result = self.json_client.mark_as_unread(safebox.guid)
        return json.loads(result)

    """
    Mark a message as read of a specific safebox associated to the current user's account.

    @param safebox:
                A Safebox object
    @param message:
                A Message object
    @return: An object containing the request result
    """
    def mark_as_read_message(self, safebox, message):
        if safebox.guid is None:
            raise SendSecureException(0, 'SafeBox GUID cannot be null', '')
        json_result = self.json_client.mark_as_read_message(safebox.guid, message.id)
        return json.loads(json_result)

    """
    Mark a message as unread of a specific safebox associated to the current user's account.

    @param safebox:
                A Safebox object
    @param message:
                A Message object
    @return: An object containing the request result
    """
    def mark_as_unread_message(self, safebox, message):
        if safebox.guid is None:
            raise SendSecureException(0, 'SafeBox GUID cannot be null', ' ')
        json_result = self.json_client.mark_as_unread_message(safebox.guid, message.id)
        return json.loads(json_result)

    """
    Retrieve a specific file url of a specific safebox associated to the current user's account.

    @param safebox:
                A Safebox object
    @param document:
                An Attachment object
    @return: The file url
    """
    def get_file_url(self, safebox, document):
        if safebox.guid is None:
            raise SendSecureException(0, 'SafeBox GUID cannot be null', '')
        if document.guid is None:
            raise SendSecureException(0, 'Document GUID cannot be null', '')
        json_result = self.json_client.get_file_url(safebox.guid, document.guid, safebox.user_email)
        result = json.loads(json_result)
        return result['url']

    """
    Retrieve the audit record url of a specific safebox associated to the current user's account.

    @param safebox:
                A Safebox object
    @return: The audit record url
    """
    def get_audit_record_url(self, safebox):
        if safebox.guid is None:
            raise SendSecureException(0, 'SafeBox GUID cannot be null', '')
        json_result = self.json_client.get_audit_record_url(safebox.guid)
        result = json.loads(json_result)
        return result['url']

    """
    Retrieve the audit record pdf of a specific safebox associated to the current user's account.

    @param safebox:
                A Safebox object
    @return: The audit record pdf stream
    """
    def get_audit_record_pdf(self, safebox):
        if safebox.guid is None:
            raise SendSecureException(0, 'SafeBox GUID cannot be null', '')
        url = self.get_audit_record_url(safebox)
        return self.json_client.get_audit_record_pdf(url)

    """
    Retrieve a filtered list of safeboxes for the current user account.

    @param url:
               The search url (optional)
    @param params:
               optional filtering parameters { status: <in_progress, closed, content_deleted or unread>,
               search_term: <search_term>, per_page: < ]0, 1000] default = 100>, page: <page to return> }
    @return: An object containing the count of found safeboxes, previous page url, the next page url and a list of Safebox objects
    """
    def get_safeboxes(self, url=None, search_params={}):
        json_result = self.json_client.get_safeboxes(url, search_params)
        result = json.loads(json_result)
        result['safeboxes'] = [Safebox(params=safebox_params['safebox']) for safebox_params in result['safeboxes']]
        return result

    """
    Retrieve a specific Safebox by its guid.

    @param safebox_guid:
                Safebox GUID
    @return: A Safebox object
    """
    def get_safebox(self, safebox_guid):
        safeboxes = self.get_safeboxes()['safeboxes']
        for safebox in safeboxes:
            if safebox.guid == safebox_guid:
                return safebox

    """
    Retrieve all info of an existing safebox for the current user account.

    @param safebox:
                A Safebox object
    @param sections:
                A string containing the list of sections to be retrieved
    @return: The updated Safebox
    """
    def get_safebox_info(self, safebox, sections=[]):
        if safebox.guid is None:
            raise SendSecureException(0, 'SafeBox GUID cannot be null', '')
        json_result = self.json_client.get_safebox_info(safebox.guid, ','.join(sections))
        result = json.loads(json_result)
        return safebox.update_attributes(result['safebox'])

    """
    Retrieve all participants info of an existing safebox for the current user account.

    @param safebox:
                A Safebox object
    @return: The list of all participants of the safebox, with all their properties
    """
    def get_safebox_participants(self, safebox):
        if safebox.guid is None:
            raise SendSecureException(0, 'SafeBox GUID cannot be null', '')
        json_result = self.json_client.get_safebox_participants(safebox.guid)
        result = json.loads(json_result)
        return [Participant(params=participant_params) for participant_params in result['participants']]

    """
    Retrieve all messages info of an existing safebox for the current user account.

    @param safebox:
                A Safebox object
    @return: The list of all messages of the safebox, with all their properties
    """
    def get_safebox_messages(self, safebox):
        if safebox.guid is None:
            raise SendSecureException(0, 'SafeBox GUID cannot be null', '')
        json_result = self.json_client.get_safebox_messages(safebox.guid)
        result = json.loads(json_result)
        return [Message(message_params) for message_params in result['messages']]

    """
    Retrieve all the security options of an existing safebox for the current user account.

    @param safebox:
                A Safebox object
    @return: All values/properties of the security options
    """
    def get_safebox_security_options(self, safebox):
        if safebox.guid is None:
            raise SendSecureException(0, 'SafeBox GUID cannot be null', '')
        json_result = self.json_client.get_safebox_security_options(safebox.guid)
        result = json.loads(json_result)
        return SecurityOptions(params=result['security_options'])

    """
    Retrieve all the download activity info of an existing safebox for the current user account.

    @param safebox:
                A Safebox object
    @return: All values/properties of the download activity
    """
    def get_safebox_download_activity(self, safebox):
        if safebox.guid is None:
            raise SendSecureException(0, 'SafeBox GUID cannot be null', '')
        json_result = self.json_client.get_safebox_download_activity(safebox.guid)
        result = json.loads(json_result)
        return DownloadActivity(result['download_activity'])

    """
    Retrieve all the event history info of an existing safebox for the current user account.

    @param safebox:
                A Safebox object
    @return: The list of all event history of the safebox, with all their properties
    """
    def get_safebox_event_history(self, safebox):
        if safebox.guid is None:
            raise SendSecureException(0, 'SafeBox GUID cannot be null', '')
        json_result = self.json_client.get_safebox_event_history(safebox.guid)
        result = json.loads(json_result)
        return [EventHistory(event_history_params) for event_history_params in result['event_history']]

    """
    Call to get the list of all the localized messages of a consent group.

    @param consent_group_id:
                      The id of the consent group
    @return: The list of all the localized messages
    """
    def get_consent_group_messages(self, consent_group_id):
        json_result = self.json_client.get_consent_group_messages(consent_group_id)
        result = json.loads(json_result)
        return ConsentMessageGroup(result["consent_message_group"])

import json
from exceptions import *

class _Enum:
    def __init__(self, values):
        for item in values.items():
            self.__dict__[item[0]] = item[1]


class JSONable:
    def __init__(self, params):

        if self._is_json(params):
            params = json.loads(params)

        self.__dict__.update(params)

        for key, value in self.__dict__.items():
            if type(value) is list:
                new_value = []
                for v in value:
                    o = self._to_object(key, v)
                    new_value.append(o if o is not None else v)
                value = new_value
            else:
                o = self._to_object(key, value)
                if o is not None:
                    value = o

            self.__dict__[key] = value

    def _is_json(self, params):
        try:
            json_object = json.loads(params)
        except TypeError, error:
            return False
        return True

    def _to_object(self, name, value):
        return None

    def _update_old_attribute(self, key, value, old_value):
        if old_value is None:
            new_value = self._to_object(key, value)
            return value if new_value is None else new_value
        elif isinstance(old_value, JSONable):
            return old_value.update_attributes(value)
        else:
            return value

    def update_attributes(self, params):
        if self._is_json(params):
            params = json.loads(params)

        for key, value in params.items():
            old_value = self.__dict__[key] if self.__dict__.has_key(key) else None
            if type(value) is list:
                if old_value is None:
                    old_value = []
                for i in range(len(value)):
                    if len(old_value) - 1 < i:
                        old_value.append(None)
                    old_value[i] = self._update_old_attribute(key, value[i], old_value[i])
            else:
                old_value = self._update_old_attribute(key, value, old_value)

            self.__dict__[key] = old_value

        return self

    def _get_ignored_keys(self):
        keys = (
            'created_at',
            'updated_at'
        )
        return keys

    def _get_sendable_keys(self):
        return None

    def to_dict(self):
        content = {}

        if self._get_sendable_keys() is None:
            keys = self.__dict__.keys()
        else:
            keys = self._get_sendable_keys()

        for key in keys:
            if key not in self._get_ignored_keys():
                value = self.__dict__.get(key)
                if value is not None:
                    if type(value) is list:
                        content[key] = []
                        for v in value:
                            content[key].append(v.to_dict() if isinstance(v, JSONable) else v)
                    else:
                        content[key] = value.to_dict() if isinstance(value, JSONable) else value

        return content

    def to_json(self):
        return json.dumps(self.to_dict(), sort_keys=True)


class Attachment(JSONable):
    def __init__(self, params):
        self.source = params['source']
        self.content_type = params.get('content_type', 'application/octet-stream')
        self.filename = params.get('filename')
        self.size = params.get('size')
        self.guid = None


class SecurityProfile(JSONable):

    TimeUnit = _Enum({
        'HOURS': 'hours',
        'DAYS': 'days',
        'WEEKS': 'weeks',
        'MONTHS': 'months'
        })

    LongTimeUnit = _Enum({
        'HOURS': 'hours',
        'DAYS': 'days',
        'WEEKS': 'weeks',
        'MONTHS': 'months',
        'YEARS': 'years',
        })

    def _to_object(self, name, value):
        if name not in ('id', 'name', 'description', 'created_at', 'updated_at'):
            return Value(value)
        else:
            return None


class Value(JSONable):
    pass


class EnterpriseSettings(JSONable):
    def _to_object(self, name, value):
        if name == 'extension_filter':
            return ExtensionFilter(value)
        else:
            return None


class ExtensionFilter(JSONable):
    pass


class UserSettings(JSONable):
    def _to_object(self, name, value):
        if name == 'secure_link':
            return PersonnalSecureLink(value)
        else:
            return None


class PersonnalSecureLink(JSONable):
    pass


class Contactable(JSONable):
    def _to_object(self, name, value):
        if name == 'contact_methods':
            return ContactMethod(value)
        else:
            return None

    def update_attributes(self, params):
        if self._is_json(params):
            params = json.loads(params)

        if params.has_key('contact_methods'):
            contacts_id = []
            for contact in params['contact_methods']:
                for key, value in contact.items():
                    if key == 'id':
                        contacts_id.append(value)

            for contact in self.__dict__['contact_methods']:
                if hasattr(contact, 'id') and contact.id not in contacts_id:
                    self.__dict__['contact_methods'].remove(contact)

        return JSONable.update_attributes(self, params)


class ContactMethod(JSONable):
    def __init__(self, params):
        JSONable.__init__(self, params)
        self._destroy = None

    DestinationType = _Enum({
        'HOME': 'home_phone',
        'CELL': 'cell_phone',
        'OFFICE': 'office_phone',
        'OTHER': 'other_phone'
        })

    def _get_sendable_keys(self):
        keys = (
            'destination',
            'destination_type',
            'id',
            '_destroy'
        )
        return keys


class Favorite(Contactable):
    def __init__(self, email=None, params=None):
        self.first_name = None
        self.last_name = None
        self.email = email
        self.company_name = None
        self.contact_methods = []

        if params is not None:
            JSONable.__init__(self, params)


    def prepare_to_destroy_contact(self, contact_method_ids):
        for contact in self.contact_methods:
            if contact.id in contact_method_ids:
                contact._destroy = True
        return self

    def _get_ignored_keys(self):
        keys = JSONable._get_ignored_keys(self)
        keys += ('id',)
        return keys

    def to_json(self):
        favorite = {'favorite': self.to_dict()}
        return json.dumps(favorite, sort_keys=True)


class Participant(JSONable):
    def __init__(self, email=None, params=None):
        self.first_name = None
        self.last_name = None
        self.email = email

        if params is not None:
            JSONable.__init__(self, params)

        if not hasattr(self, 'guest_options'):
            self.guest_options = GuestOptions()

    def _to_object(self, name, value):
        if name == 'guest_options':
            return GuestOptions(value)
        else:
            return None

    def to_dict(self):
        content = JSONable.to_dict(self)
        options = self.guest_options.to_dict()
        content.update(options)

        return content

    def _get_sendable_keys(self):
        keys = (
            'first_name',
            'last_name',
            'email'
        )
        return keys

    def prepare_to_destroy_contact(self, contact_method_ids):
        for contact in self.guest_options.contact_methods:
            if contact.id in contact_method_ids:
                contact._destroy = '1'
        return self

    def to_json(self):
        participant = {'participant': self.to_dict()}
        return json.dumps(participant, sort_keys=True)


class GuestOptions(Contactable):
    def __init__(self, params=None):
        self.contact_methods = []
        self.company_name = None
        self.locked = None

        if params is not None:
            JSONable.__init__(self, params)


    def _get_ignored_keys(self):
        keys = JSONable._get_ignored_keys(self)
        keys += ('bounced_email', 'failed_login_attempts', 'verified',)
        return keys


class Safebox(JSONable):
    def __init__(self, user_email=None, notification_language="en", params=None):
        self.participants = []
        self.subject = None
        self.message = None
        self.attachments = []
        self.security_profile_id = None
        self.user_email = user_email
        self.notification_language = notification_language
        self.email_notification_enabled = None

        if params is not None:
            JSONable.__init__(self, params)

        if not hasattr(self, 'security_options'):
            self.security_options = SecurityOptions()

    def _to_object(self, name, value):
        if name == 'security_options':
            return SecurityOptions(value)
        elif name == 'download_activity':
            return DownloadActivity(value)
        elif name == 'messages':
            return Message(value)
        elif name == 'participants':
            return Participant(params=value)
        elif name == 'event_history':
            return EventHistory(value)
        else:
            return None

    def _get_sendable_keys(self):
        keys = (
            'guid',
            'subject',
            'message',
            'security_profile_id',
            'public_encryption_key',
            'notification_language',
            'user_email',
            'email_notification_enabled'
        )
        return keys

    def update_attributes(self, params):
        if self._is_json(params):
            params = json.loads(params)

        if params.has_key('is_creation'):
            params['security_options'] = {}
            for key in self._get_security_options_keys():
                if key in params.keys():
                    params['security_options'][key] = params[key]
                    del params[key]
            del params['is_creation']

        return JSONable.update_attributes(self, params)

    def set_expiration_values(self, date_time):
        if hasattr(self, 'status'):
            raise SendSecureException(0, 'Cannot change the expiration of a committed safebox, please see the method addTime to extend the lifetime of the safebox', '')
        self.security_options.expiration_date = date_time.strftime('%Y-%m-%d')
        self.security_options.expiration_time = date_time.strftime('%H:%M:%S')
        self.security_options.expiration_time_zone = date_time.strftime('%z')

    def _get_security_options_keys(self):
        keys = (
            'security_code_length',
            'allowed_login_attempts',
            'allow_remember_me',
            'allow_sms',
            'allow_voice',
            'allow_email',
            'reply_enabled',
            'group_replies',
            'code_time_limit',
            'encrypt_message',
            'two_factor_required',
            'auto_extend_value',
            'auto_extend_unit',
            'retention_period_type',
            'retention_period_value',
            'retention_period_unit',
            'allow_manual_delete',
            'allow_manual_close'
        )
        return keys

    def to_dict(self):
        content = JSONable.to_dict(self)

        content['recipients'] = []
        for item in self.participants:
            if not hasattr(item, 'type') or item.type == "guest":
                content['recipients'].append(item.to_dict())

        self._append_document_ids_to_dict(content)

        content.update(self.security_options.to_dict())

        return content

    def _append_document_ids_to_dict(self, content):
        content['document_ids'] = []
        if hasattr(self, 'attachments'):
            for item in self.attachments:
                content['document_ids'].append(item.guid)

    def _temporary_document(self, file_size):
        if hasattr(self, 'public_encryption_key'):
            return { "temporary_document": { "document_file_size": file_size },
                     "multipart": False,
                     "public_encryption_key": self.public_encryption_key
                    }
        return { "temporary_document": { "document_file_size": file_size },
                 "multipart": False
                }

    def to_json(self):
        safebox = {'safebox': self.to_dict()}
        return json.dumps(safebox, sort_keys=True)


class DownloadActivity(JSONable):
    def _to_object(self, name, value):
        return DownloadActivityDetail(value)


class DownloadActivityDetail(JSONable):
    def _to_object(self, name, value):
        if name == 'documents':
            return Document(value)
        else:
            return None


class Document(JSONable):
    pass


class EventHistory(JSONable):
    pass


class Message(JSONable):
    def _to_object(self, name, value):
        if name == 'documents':
            return Document(value)
        else:
            return None


class SecurityOptions(JSONable):
    def __init__(self, params=None):
        self.reply_enabled = None
        self.group_replies = None
        self.retention_period_type = None
        self.retention_period_value = None
        self.retention_period_unit = None
        self.encrypt_message = None
        self.double_encryption = None
        self.expiration_value = None
        self.expiration_unit = None
        self.expiration_date = None
        self.expiration_time = None
        self.expiration_time_zone = None

        if params is not None:
            JSONable.__init__(self, params)


    def _get_sendable_keys(self):
        keys = (
            'reply_enabled',
            'group_replies',
            'retention_period_type',
            'retention_period_value',
            'retention_period_unit',
            'encrypt_message',
            'double_encryption',
            'expiration_value',
            'expiration_unit',
            'expiration_date',
            'expiration_time',
            'expiration_time_zone'
        )
        return keys

class Reply(JSONable):
    def __init__(self, params=None):
        self.message = None
        self.consent = None #Optional
        self.attachments = []
        self.document_ids = []

        if params is not None:
            JSONable.__init__(self, params)

    def _get_sendable_keys(self):
        keys = (
            'message',
            'consent',
            'document_ids'
        )
        return keys

    def to_json(self):
        return json.dumps({'safebox' : self.to_dict()}, sort_keys=True)

class ConsentMessage(JSONable):
    pass

class ConsentMessageGroup(JSONable):
    def _to_object(self, name, value):
        if name == 'consent_messages':
            return ConsentMessage(value)
        else:
            return None
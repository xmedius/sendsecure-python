import json

class _Enum:
    def __init__(self, values):
        for item in values.items():
            self.__dict__[item[0]] = item[1]


class Attachment:
    def __init__(self, source, content_type='application/octet-stream', filename=None, size=None):
        self.source = source
        self.content_type = content_type
        self.filename = filename
        self.size = size
        self.guid = None


class ContactMethod:

    DestinationType = _Enum( {
        'HOME' : 'home_phone',
        'CELL' : 'cell_phone',
        'OFFICE' : 'office_phone',
        'OTHER' : 'other_phone'
        } )

    def __init__(self, destination, destination_type=DestinationType.CELL):
        self.destination = destination
        self.destination_type = destination_type

    def to_dict(self):
        content = {}
        for name in ('destination', 'destination_type'):
            content[name] = self.__dict__[name]
        return content

    def to_json(self):
        return json.dumps(self.to_dict())


class Recipient:
    def __init__(self, email, first_name=None, last_name=None, company_name=None, contact_methods=None):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.company_name = company_name
        self.contact_methods = contact_methods or []

    def to_dict(self):
        content = {}
        for name in ('first_name', 'last_name', 'company_name', 'email'):
            content[name] = self.__dict__[name]

        content['contact_methods'] = []
        for item in self.contact_methods:
            content['contact_methods'].append(item.to_dict())

        return content

    def to_json(self):
        return json.dumps(self.to_dict())


class Safebox:
    def __init__(self, user_email, subject=None, message=None, security_profile=None, recipients = None, attachments = None, notification_language='en'):
        self.user_email = user_email
        self.subject = subject
        self.message = message
        self.notification_language = notification_language
        self.guid = None
        self.public_encryption_key = None
        self.upload_url = None
        self.recipients = recipients or []
        self.attachments = attachments or []
        self.security_profile = security_profile

    def to_dict(self):
        content = {}
        for name in ('subject', 'message', 'notification_language', 'guid', 'public_encryption_key'):
            content[name] = self.__dict__[name]

        content['recipients'] = []
        for item in self.recipients:
            content['recipients'].append(item.to_dict())

        content['document_ids'] = []
        for item in self.attachments:
            content['document_ids'].append(item.guid)

        if self.security_profile:
            content['security_profile_id'] = self.security_profile.id
            content['reply_enabled'] = self.security_profile.reply_enabled.value
            content['group_replies'] = self.security_profile.group_replies.value
            content['expiration_value'] = self.security_profile.expiration_value.value
            content['expiration_unit'] = self.security_profile.expiration_unit.value
            content['retention_period_type'] = self.security_profile.retention_period_type.value
            content['retention_period_value'] = self.security_profile.retention_period_value.value
            content['retention_period_unit'] = self.security_profile.retention_period_unit.value
            content['encrypt_message'] = self.security_profile.encrypt_message.value
            content['double_encryption'] = self.security_profile.double_encryption.value

        return content

    def to_json(self):
        safebox = {'safebox' : self.to_dict(), 'user_email' : self.user_email}
        return json.dumps(safebox)


class SafeboxResponse:
    @staticmethod
    def from_json(json_format):
        return SafeboxResponse(json_format)

    def __init__(self, json_format):
        #avoid calling __setattr__ on j
        self.__dict__['j'] = json.loads(json_format)

    def __setattr__(self, attribute, value):
        self.j[attribute] = value

    def __getattr__(self, attribute):
        try:
            return self.j[attribute]
        except:
            raise AttributeError

    def to_json(self):
        return json.dumps(self.j)


class SecurityProfile:

    TimeUnit = _Enum( {
        'HOURS' : 'hours',
        'DAYS' : 'days',
        'WEEKS' : 'weeks',
        'MONTHS' : 'months'
        } )

    LongTimeUnit = _Enum( {
        'HOURS' : 'hours',
        'DAYS' : 'days',
        'WEEKS' : 'weeks',
        'MONTHS' : 'months',
        'YEARS' : 'years',
        } )

    @staticmethod
    def from_json(json_format):
        return SecurityProfile(json_format)

    def __init__(self, json_format):
        j = json.loads(json_format)
        #avoid calling __setattr__ on j
        self.__dict__['j'] = j
        for name in self._get_value_names():
            self.__dict__[name] = Value(j[name]['modifiable'], j[name]['value'])

    def __setattr__(self, attribute, value):
        self.j[attribute] = value

    def __getattr__(self, attribute):
        try:
            return self.j[attribute]
        except:
            raise AttributeError

    def _get_value_names(self):
        values = (
            'allowed_login_attempts',
            'allow_remember_me',
            'allow_sms',
            'allow_voice',
            'allow_email',
            'code_time_limit',
            'code_length',
            'auto_extend_value',
            'auto_extend_unit',
            'two_factor_required',
            'encrypt_attachments',
            'encrypt_message',
            'expiration_value',
            'expiration_unit',
            'reply_enabled',
            'group_replies',
            'double_encryption',
            'retention_period_value',
            'retention_period_unit',
            'retention_period_type'
        )
        return values

    def to_dict(self):
        for name in _get_value_names():
            self.j[name]['modifiable'] = self.__dict__[name].modifiable
            self.j[name]['value'] = self.__dict__[name].value
        return self.j

    def to_json(self):
        return json.dumps(self.to_dict())


class Value:
    def __init__(self, modifiable, value):
        self.modifiable = modifiable
        self.value = value


class EnterpriseSettings:
    @staticmethod
    def from_json(json_format):
        return EnterpriseSettings(json_format)

    def __init__(self, json_format):
        #avoid calling __setattr__ on j
        self.__dict__['j'] = json.loads(json_format)
        self.__dict__['extension_filter'] = ExtensionFilter(self.j['extension_filter']['mode'], self.j['extension_filter']['list'])

    def __setattr__(self, attribute, value):
        self.j[attribute] = value

    def __getattr__(self, attribute):
        try:
            return self.j[attribute]
        except:
            raise AttributeError

    def to_dict(self):
        self.j['extension_filter']['mode'] = self.extension_filter.mode
        self.j['extension_filter']['list'] = self.extension_filter.list
        return self.j

    def to_json(self):
        return json.dumps(self.to_dict())


class ExtensionFilter:
    def __init__(self, filter_mode, filter_list):
        self.mode = filter_mode
        self.list = filter_list

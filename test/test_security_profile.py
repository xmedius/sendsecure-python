from sendsecure import *
import unittest

class TestSecurityProfile(unittest.TestCase):
    security_profile_params = { 'id': 10,
                                'name': 'email-only',
                                'description': '',
                                'created_at': '2016-04-27T21:08:29.457Z',
                                'updated_at': '2016-07-27T19:03:05.883Z',
                                'allowed_login_attempts': {'value': 3, 'modifiable': False},
                                'allow_remember_me': {'value': False, 'modifiable': False},
                                'allow_sms': {'value': False, 'modifiable': False},
                                'allow_voice': {'value': False, 'modifiable': False},
                                'allow_email': {'value': True, 'modifiable': False},
                                'code_time_limit': {'value': 5, 'modifiable': False},
                                'code_length': {'value': 4, 'modifiable': False},
                                'auto_extend_value': {'value': 3, 'modifiable': False},
                                'auto_extend_unit': {'value': 'days', 'modifiable': False},
                                'two_factor_required': {'value': True, 'modifiable': False},
                                'encrypt_attachments': {'value': True, 'modifiable': False},
                                'encrypt_message': {'value': False, 'modifiable': False},
                                'expiration_value': {'value': 7, 'modifiable': False},
                                'expiration_unit': {'value': 'hours', 'modifiable': False},
                                'reply_enabled': {'value': True, 'modifiable': False},
                                'group_replies': {'value': False, 'modifiable': False},
                                'double_encryption': {'value': True, 'modifiable': False},
                                'retention_period_type': {'value': 'discard_at_expiration', 'modifiable': False},
                                'retention_period_value': {'value': None, 'modifiable': False},
                                'retention_period_unit': {'value': None, 'modifiable': False}
                              }

    def setUp(self):
        pass

    def test_initialization_with_params(self):
        security_profile = SecurityProfile(self.security_profile_params)
        self.assertEqual(security_profile.id, 10)
        self.assertEqual(security_profile.name, 'email-only')
        self.assertEqual(security_profile.description, '')
        self.assertEqual(security_profile.created_at, '2016-04-27T21:08:29.457Z')
        self.assertEqual(security_profile.updated_at, '2016-07-27T19:03:05.883Z')
        self.assertIsInstance(security_profile.allowed_login_attempts, Value)
        self.assertIsInstance(security_profile.allow_remember_me, Value)
        self.assertIsInstance(security_profile.allow_sms, Value)
        self.assertIsInstance(security_profile.allow_voice, Value)
        self.assertIsInstance(security_profile.allow_email, Value)
        self.assertIsInstance(security_profile.code_time_limit, Value)
        self.assertIsInstance(security_profile.code_length, Value)
        self.assertIsInstance(security_profile.auto_extend_value, Value)
        self.assertIsInstance(security_profile.auto_extend_unit, Value)
        self.assertIsInstance(security_profile.two_factor_required, Value)
        self.assertIsInstance(security_profile.encrypt_attachments, Value)
        self.assertIsInstance(security_profile.encrypt_message, Value)
        self.assertIsInstance(security_profile.expiration_value, Value)
        self.assertIsInstance(security_profile.expiration_unit, Value)
        self.assertIsInstance(security_profile.reply_enabled, Value)
        self.assertIsInstance(security_profile.group_replies, Value)
        self.assertIsInstance(security_profile.double_encryption, Value)
        self.assertIsInstance(security_profile.retention_period_type, Value)
        self.assertIsInstance(security_profile.retention_period_value, Value)
        self.assertIsInstance(security_profile.retention_period_unit, Value)

    def test_initialization_with_json_params(self):
        security_profile = SecurityProfile(self.security_profile_params)
        self.assertEqual(security_profile.id, 10)
        self.assertEqual(security_profile.name, 'email-only')
        self.assertEqual(security_profile.description, '')
        self.assertEqual(security_profile.created_at, '2016-04-27T21:08:29.457Z')
        self.assertEqual(security_profile.updated_at, '2016-07-27T19:03:05.883Z')
        self.assertIsInstance(security_profile.allowed_login_attempts, Value)
        self.assertIsInstance(security_profile.allow_remember_me, Value)
        self.assertIsInstance(security_profile.allow_sms, Value)
        self.assertIsInstance(security_profile.allow_voice, Value)
        self.assertIsInstance(security_profile.allow_email, Value)
        self.assertIsInstance(security_profile.code_time_limit, Value)
        self.assertIsInstance(security_profile.code_length, Value)
        self.assertIsInstance(security_profile.auto_extend_value, Value)
        self.assertIsInstance(security_profile.auto_extend_unit, Value)
        self.assertIsInstance(security_profile.two_factor_required, Value)
        self.assertIsInstance(security_profile.encrypt_attachments, Value)
        self.assertIsInstance(security_profile.encrypt_message, Value)
        self.assertIsInstance(security_profile.expiration_value, Value)
        self.assertIsInstance(security_profile.expiration_unit, Value)
        self.assertIsInstance(security_profile.reply_enabled, Value)
        self.assertIsInstance(security_profile.group_replies, Value)
        self.assertIsInstance(security_profile.double_encryption, Value)
        self.assertIsInstance(security_profile.retention_period_type, Value)
        self.assertIsInstance(security_profile.retention_period_value, Value)
        self.assertIsInstance(security_profile.retention_period_unit, Value)

if __name__ == '__main__':
    unittest.main()
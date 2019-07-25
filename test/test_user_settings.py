from sendsecure import *
import unittest

class TestUserSettings(unittest.TestCase):
    user_settings_params = { 'created_at': '2016-08-15T21:56:45.798Z',
                             'updated_at': '2017-04-10T18:58:59.356Z',
                             'mask_note': False,
                             'open_first_transaction': False,
                             'mark_as_read': True,
                             'mark_as_read_delay': 5,
                             'remember_key': True,
                             'default_filter': 'everything',
                             'recipient_language': None,
                             'secure_link': {
                               'enabled': True,
                               'url': 'https://sendsecure.integration.xmedius.com/r/6125b3f',
                               'security_profile_id': 1 },
                             'always_promote_as_privileged': True
                            }
    def test_initialization_with_params(self):
        user_settings = UserSettings(self.user_settings_params)
        self.assertEqual(user_settings.created_at, '2016-08-15T21:56:45.798Z')
        self.assertEqual(user_settings.updated_at, '2017-04-10T18:58:59.356Z')
        self.assertFalse(user_settings.mask_note)
        self.assertFalse(user_settings.open_first_transaction)
        self.assertTrue(user_settings.mark_as_read)
        self.assertEqual(user_settings.mark_as_read_delay, 5)
        self.assertTrue(user_settings.remember_key)
        self.assertEqual(user_settings.default_filter, 'everything')
        self.assertIsNone(user_settings.recipient_language)
        secure_link = user_settings.secure_link
        self.assertIsInstance(secure_link, PersonnalSecureLink)
        self.assertTrue(secure_link.enabled)
        self.assertEqual(secure_link.url, 'https://sendsecure.integration.xmedius.com/r/6125b3f')
        self.assertEqual(secure_link.security_profile_id, 1)
        self.assertTrue(user_settings.always_promote_as_privileged)

    def test_initialization_with_json_params(self):
        user_settings = UserSettings(json.dumps(self.user_settings_params))
        self.assertEqual(user_settings.created_at, '2016-08-15T21:56:45.798Z')
        self.assertEqual(user_settings.updated_at, '2017-04-10T18:58:59.356Z')
        self.assertFalse(user_settings.mask_note)
        self.assertFalse(user_settings.open_first_transaction)
        self.assertTrue(user_settings.mark_as_read)
        self.assertEqual(user_settings.mark_as_read_delay, 5)
        self.assertTrue(user_settings.remember_key)
        self.assertEqual(user_settings.default_filter, 'everything')
        self.assertIsNone(user_settings.recipient_language)
        secure_link = user_settings.secure_link
        self.assertIsInstance(secure_link, PersonnalSecureLink)
        self.assertTrue(secure_link.enabled)
        self.assertEqual(secure_link.url, 'https://sendsecure.integration.xmedius.com/r/6125b3f')
        self.assertEqual(secure_link.security_profile_id, 1)
        self.assertTrue(user_settings.always_promote_as_privileged)

if __name__ == '__main__':
    unittest.main()
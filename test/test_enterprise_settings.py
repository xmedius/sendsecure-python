from sendsecure import *
import unittest

class TestEnterpriseSettings(unittest.TestCase):
    enterprise_settings_params = { 'created_at': '2016-04-27T21:08:29.457Z',
                                   'updated_at': '2016-07-27T19:03:05.883Z',
                                   'default_security_profile_id': 1,
                                   'pdf_language': 'en',
                                   'use_pdfa_audit_records': False,
                                   'international_dialing_plan': 'ca',
                                   'extension_filter': { 'mode': 'forbid',
                                                         'list': ['bin', 'bat'] },
                                   'virus_scan_enabled': False,
                                   'max_file_size_value': None,
                                   'max_file_size_unit': None,
                                   'include_users_in_autocomplete': True,
                                   'include_favorites_in_autocomplete': True,
                                   'users_public_url': True
                                 }

    def setUp(self):
        pass

    def test_initialization_with_params(self):
        enterprise_settings = EnterpriseSettings(self.enterprise_settings_params)
        self.assertEqual(enterprise_settings.created_at, '2016-04-27T21:08:29.457Z')
        self.assertEqual(enterprise_settings.updated_at, '2016-07-27T19:03:05.883Z')
        self.assertEqual(enterprise_settings.default_security_profile_id, 1)
        self.assertEqual(enterprise_settings.pdf_language, 'en')
        self.assertFalse(enterprise_settings.use_pdfa_audit_records)
        self.assertEqual(enterprise_settings.international_dialing_plan, 'ca')
        self.assertIsInstance(enterprise_settings.extension_filter, ExtensionFilter)
        self.assertEqual(enterprise_settings.extension_filter.mode, 'forbid')
        self.assertTrue(enterprise_settings.extension_filter.list)
        self.assertFalse(enterprise_settings.virus_scan_enabled)
        self.assertIsNone(enterprise_settings.max_file_size_value)
        self.assertIsNone(enterprise_settings.max_file_size_unit)
        self.assertTrue(enterprise_settings.include_users_in_autocomplete)
        self.assertTrue(enterprise_settings.include_favorites_in_autocomplete)
        self.assertTrue(enterprise_settings.users_public_url)

    def test_initialization_with_json_params(self):
        enterprise_settings = EnterpriseSettings(json.dumps(self.enterprise_settings_params))
        self.assertEqual(enterprise_settings.created_at, '2016-04-27T21:08:29.457Z')
        self.assertEqual(enterprise_settings.updated_at, '2016-07-27T19:03:05.883Z')
        self.assertEqual(enterprise_settings.default_security_profile_id, 1)
        self.assertEqual(enterprise_settings.pdf_language, 'en')
        self.assertFalse(enterprise_settings.use_pdfa_audit_records)
        self.assertEqual(enterprise_settings.international_dialing_plan, 'ca')
        self.assertIsInstance(enterprise_settings.extension_filter, ExtensionFilter)
        self.assertEqual(enterprise_settings.extension_filter.mode, 'forbid')
        self.assertTrue(enterprise_settings.extension_filter.list)
        self.assertFalse(enterprise_settings.virus_scan_enabled)
        self.assertIsNone(enterprise_settings.max_file_size_value)
        self.assertIsNone(enterprise_settings.max_file_size_unit)
        self.assertTrue(enterprise_settings.include_users_in_autocomplete)
        self.assertTrue(enterprise_settings.include_favorites_in_autocomplete)
        self.assertTrue(enterprise_settings.users_public_url)

if __name__ == '__main__':
    unittest.main()

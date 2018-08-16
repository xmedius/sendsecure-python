from sendsecure import *
import unittest
try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock

class TestClient(unittest.TestCase):
    client = Client({ 'token': 'USER|489b3b1f-b411-428e-be5b-2abbace87689',
                      'user_id': '123456',
                      'enterprise_account': 'acme',
                      'endpoint': 'https://awesome.portal' })
    safebox = Safebox(params=json.dumps({ 'guid': '1c820789a50747df8746aa5d71922a3f',
                                          'user_email': 'user@acme.com',
                                          'participants': [
                                              { 'email': 'recipient@test.xmedius.com',
                                                'guest_options': {
                                                    'contact_methods': [
                                                        { 'destination_type': 'cell_phone',
                                                          'destination': '+15145550000' }
                                                    ]
                                                }
                                              }
                                          ],
                                          'expiration': '2016-12-06T05:38:09.951Z',
                                          'notification_language': 'en',
                                          'status': 'in_progress'
                                          }))

    def test_get_enterprise_settings(self):
        expected_response = json.dumps({ 'created_at': '2016-03-15T19:58:11.588Z',
                                         'updated_at': '2016-09-28T18:32:16.643Z',
                                         'default_security_profile_id': 10 })
        self.client.json_client.get_enterprise_settings = Mock(return_value=expected_response)
        result = self.client.get_enterprise_settings()
        self.assertIsInstance(result, EnterpriseSettings)
        self.assertEqual(result.default_security_profile_id, 10)

    def test_get_security_profiles(self):
        expected_response = json.dumps({ 'security_profiles': [{ 'id': 5 }, { 'id': 10 }] })
        self.client.json_client.get_security_profiles = Mock(return_value=expected_response)
        result = self.client.get_security_profiles('user@example.com')
        self.client.json_client.get_security_profiles.assert_called_once_with('user@example.com')
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], SecurityProfile)
        self.assertEqual(result[0].id, 5)
        self.assertIsInstance(result[1], SecurityProfile)
        self.assertEqual(result[1].id, 10)

    def test_get_default_security_profile(self):
        enterprise_settings_response = json.dumps({ 'created_at': '2016-03-15T19:58:11.588Z',
                                         'updated_at': '2016-09-28T18:32:16.643Z',
                                         'default_security_profile_id': 10 })
        security_profiles_response = json.dumps({ 'security_profiles': [{ 'id': 5 }, { 'id': 10 }] })
        self.client.json_client.get_enterprise_settings = Mock(return_value=enterprise_settings_response)
        self.client.json_client.get_security_profiles = Mock(return_value=security_profiles_response)
        result = self.client.get_default_security_profile('user@example.com')
        self.client.json_client.get_security_profiles.assert_called_once_with('user@example.com')
        self.assertIsInstance(result, SecurityProfile)
        self.assertEqual(result.id, 10)

    def test_submit_safebox(self):
        safebox = Safebox(params=json.dumps({ 'user_email': 'user@acme.com',
                                              'participants': [
                                                  { 'email': 'recipient@test.xmedius.com',
                                                    'guest_options': {
                                                    'contact_methods': [
                                                        { 'destination_type': 'cell_phone',
                                                          'destination': '+15145550000' }]
                                                    }
                                                  }],
                                              'message': 'lorem ipsum...',
                                              'notification_language': 'en' }))
        attachment = Attachment({'source': 'simple.pdf', 'content_type': 'application/pdf'})
        safebox.attachments.append(attachment)
        expected_response = json.dumps({ 'guid': '1c820789a50747df8746aa5d71922a3f',
                                         'user_id': 3,
                                         'enterprise_id': 1,
                                         'subject': None,
                                         'expiration': '2016-12-06T05:38:09.951Z',
                                         'notification_language': 'en',
                                         'status': 'in_progress',
                                         'security_profile_name': 'email-only',
                                         'force_expiry_date': None,
                                         'security_code_length': 4,
                                         'allowed_login_attempts': 3,
                                         'allow_remember_me': False,
                                         'allow_sms': False,
                                         'allow_voice': False,
                                         'allow_email': True,
                                         'reply_enabled': True,
                                         'group_replies': False,
                                         'code_time_limit': 5,
                                         'encrypt_message': False,
                                         'two_factor_required': True,
                                         'auto_extend_value': 3,
                                         'auto_extend_unit': 'days',
                                         'retention_period_type': 'discard_at_expiration',
                                         'retention_period_value': None,
                                         'retention_period_unit': None,
                                         'delete_content_on': None,
                                         'preview_url': 'http://sendsecure.lvh.me:3001/s/5b8e88acc9c44b229ba64256298f9388/preview?k=AyOmyAawJXKepb9LuJAOyiJXvkpEQcdSweS2-It3jaRntO9rRyCaciv7QBt5Dqoz',
                                         'encryption_key': 'AyOmyAawJXKepb9LuJAOyiJXvkpEQcdSweS2-It3jaRntO9rRyCaciv7QBt5Dqoz',
                                         'created_at': '2016-12-05T22:38:09.965Z',
                                         'updated_at': '2016-12-05T22:38:09.965Z',
                                         'latest_activity': '2016-12-05T22:38:10.068Z'
                                       })
        initialize_safebox_response = json.dumps({ 'guid': '1c820789a50747df8746aa5d71922a3f', 'public_encryption_key': 'AyOmyAawJXKepb9LuJAOyiJXvkpEQcdSweS2-It3jaRntO9rRyCaciv7QBt5Dqoz', 'upload_url': 'upload_url'})
        upload_attachment_response = json.dumps({ 'temporary_document': { 'document_guid': '5d4d6a8158b04915a532622983eb4493' } })
        enterprise_settings_response = json.dumps({ 'created_at': '2016-03-15T19:58:11.588Z',
                                         'updated_at': '2016-09-28T18:32:16.643Z',
                                         'default_security_profile_id': 10 })
        security_profiles_response = json.dumps({ 'security_profiles': [{ 'id': 5 }, { 'id': 10 }] })
        self.client.json_client.get_enterprise_settings = Mock(return_value=enterprise_settings_response)
        self.client.json_client.get_security_profiles = Mock(return_value=security_profiles_response)
        self.client.json_client.new_safebox = Mock(return_value=initialize_safebox_response)
        self.client.json_client.upload_file = Mock(return_value=upload_attachment_response)
        self.client.json_client.commit_safebox = Mock(return_value=expected_response)
        result = self.client.submit_safebox(safebox)
        self.client.json_client.new_safebox.assert_called_once_with('user@acme.com')
        self.client.json_client.get_security_profiles.assert_called_once_with('user@acme.com')
        self.assertIsInstance(result, Safebox)
        self.assertEqual(result.guid, '1c820789a50747df8746aa5d71922a3f')

    def test_commit_safebox_should_fail_when_guid_is_missing(self):
        safebox = Safebox(params=json.dumps({ 'guid': None,
                                              'user_email': 'user@acme.com',
                                              'participants': [
                                                  { 'email': 'recipient@test.xmedius.com',
                                                    'guest_options': {
                                                    'contact_methods': [
                                                        { 'destination_type': 'cell_phone',
                                                          'destination': '+15145550000' }]
                                                    }
                                                  }],
                                              'message': 'lorem ipsum...',
                                              'notification_language': 'en' }))
        with self.assertRaises(SendSecureException) as context:
            result = self.client.commit_safebox(safebox)
        self.assertIn('SafeBox GUID cannot be null', context.exception.message)

    def test_commit_safebox_should_fail_when_recipients_are_missing(self):
        safebox = Safebox(params=json.dumps({ 'guid': 'ewtwewtegew54gwe68ef8w4',
                                              'user_email': 'user@acme.com',
                                              'participants': [],
                                              'message': 'lorem ipsum...',
                                              'notification_language': 'en' }))
        with self.assertRaises(SendSecureException) as context:
            result = self.client.commit_safebox(safebox)
        self.assertIn('Participants cannot be empty', context.exception.message)

    def test_commit_safebox_should_fail_when_security_profile_id_is_missing(self):
        safebox = Safebox(params=json.dumps({ 'guid': 'ewtwewtegew54gwe68ef8w4',
                                              'user_email': 'user@acme.com',
                                              'participants': [
                                                  { 'email': 'recipient@test.xmedius.com',
                                                    'guest_options': {
                                                    'contact_methods': [
                                                        { 'destination_type': 'cell_phone',
                                                          'destination': '+15145550000' }]
                                                    }
                                                  }],
                                              'message': 'lorem ipsum...',
                                              'notification_language': 'en',
                                              'security_profile_id': None }))
        with self.assertRaises(SendSecureException) as context:
            result = self.client.commit_safebox(safebox)
        self.assertIn('No Security Profile configured', context.exception.message)

    def test_get_user_settings(self):
        expected_response = json.dumps({ 'created_at': '2016-03-15T19:58:11.588Z',
                                         'updated_at': '2016-09-28T18:32:16.643Z',
                                         'default_filter': 'unread' })
        self.client.json_client.get_user_settings = Mock(return_value= expected_response)
        result = self.client.get_user_settings()
        self.assertIsInstance(result, UserSettings)
        self.assertEqual(result.created_at, '2016-03-15T19:58:11.588Z')
        self.assertEqual(result.updated_at, '2016-09-28T18:32:16.643Z')
        self.assertEqual(result.default_filter, 'unread')

    def test_get_favorites(self):
        expected_response = json.dumps({ 'favorites': [
                                            { 'email': 'john.smith@example.com',
                                              'id': 456 },
                                            { 'email': 'jane.doe@example.com',
                                              'id': 789 } ] })
        self.client.json_client.get_favorites = Mock(return_value=expected_response)
        result = self.client.get_favorites()
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], Favorite)
        self.assertIsInstance(result[1], Favorite)

    def test_create_favorite(self):
        favorite = Favorite(params=json.dumps({ 'email': 'john.smith@example.com',
                                                'first_name': '',
                                                'last_name': 'Smith',
                                                'company_name': 'Acme',
                                                'contact_methods': [{
                                                    'destination': '+15145550000',
                                                    'destination_type': 'office_phone' }]
                                              }))
        expected_response = json.dumps({ 'email': 'john.smith@example.com',
                                          'id': 456,
                                          'first_name': '',
                                          'last_name': 'Smith',
                                          'company_name': 'Acme',
                                          'order_number': 10,
                                          'created_at': '2016-04-19T16:26:18.277Z',
                                          'updated_at': '2016-09-07T19:33:51.192Z',
                                          'contact_methods': [{
                                              'id': 1,
                                              'destination': '+15145550000',
                                              'destination_type': 'office_phone',
                                              'created_at': '2017-04-28T17:14:55.304Z',
                                              'updated_at': '2017-04-28T17:14:55.304Z'
                                          }]
                                       })
        self.client.json_client.create_favorite = Mock(return_value=expected_response)
        self.client.create_favorite(favorite)
        self.assertEqual(favorite.id, 456)
        self.assertEqual(favorite.order_number, 10)
        self.assertTrue(favorite.contact_methods)
        self.assertEqual(favorite.contact_methods[0].id, 1)
        self.assertEqual(favorite.created_at, '2016-04-19T16:26:18.277Z')
        self.assertEqual(favorite.updated_at, '2016-09-07T19:33:51.192Z')
        self.assertEqual(favorite.contact_methods[0].created_at, '2017-04-28T17:14:55.304Z')
        self.assertEqual(favorite.contact_methods[0].updated_at, '2017-04-28T17:14:55.304Z')

    def test_create_favorite_should_fail_when_email_is_missing(self):
        favorite = Favorite(params=json.dumps({ 'email': None,
                                                'first_name': '',
                                                'last_name': 'Smith',
                                                'company_name': 'Acme',
                                                'contact_methods': [{
                                                    'destination': '+15145550000',
                                                    'destination_type': 'office_phone' }]
                                              }))
        with self.assertRaises(SendSecureException) as context:
            result = self.client.create_favorite(favorite)
        self.assertIn('Favorite email cannot be null', context.exception.message)

    def test_update_favorite(self):
        favorite = Favorite(params=json.dumps({ 'email': 'john.smith@example.com',
                                                'id': 456,
                                                'last_name': 'Smith',
                                                'company_name': 'Acme',
                                                'order_number': 10,
                                                'contact_methods': [{
                                                    'id': 1,
                                                    'destination': '+15145550000',
                                                    'destination_type': 'office_phone' }]
                                              }))
        expected_response = json.dumps({ 'email': 'john.smith@example.com',
                                         'id': 456,
                                         'first_name': '',
                                         'last_name': 'Smith',
                                         'company_name': 'Acme',
                                         'order_number': 10,
                                         'created_at': '2016-04-19T16:26:18.277Z',
                                         'updated_at': '2016-09-07T19:33:51.192Z',
                                         'contact_methods': [{
                                             'id': 1,
                                             'destination': '+15145550000',
                                             'destination_type': 'office_phone',
                                             'created_at': '2017-04-28T17:14:55.304Z',
                                             'updated_at': '2017-04-28T17:14:55.304Z' }]
                                       })
        self.client.json_client.update_favorite = Mock(return_value=expected_response)
        self.client.update_favorite(favorite)
        self.assertEqual(favorite.id, 456)
        self.assertEqual(favorite.order_number, 10)
        self.assertTrue(favorite.contact_methods)
        self.assertEqual(favorite.contact_methods[0].id, 1)
        self.assertEqual(favorite.created_at, '2016-04-19T16:26:18.277Z')
        self.assertEqual(favorite.updated_at, '2016-09-07T19:33:51.192Z')
        self.assertEqual(favorite.contact_methods[0].created_at, '2017-04-28T17:14:55.304Z')
        self.assertEqual(favorite.contact_methods[0].updated_at, '2017-04-28T17:14:55.304Z')

    def test_update_favorite_should_fail_when_id_is_missing(self):
        favorite = Favorite(params=json.dumps({ 'email': 'john.smith@example.com',
                                                'id': None,
                                                'last_name': 'Smith',
                                                'company_name': 'Acme',
                                                'order_number': 10,
                                                'contact_methods': [{
                                                    'id': 1,
                                                    'destination': '+15145550000',
                                                    'destination_type': 'office_phone' }]
                                              }))
        with self.assertRaises(SendSecureException) as context:
            self.client.update_favorite(favorite)
        self.assertIn('Favorite id cannot be null', context.exception.message)

    def test_delete_favorite_contact_methods(self):
        favorite = Favorite(params=json.dumps({ 'email': 'john.smith@example.com',
                                                'id': 456,
                                                'last_name': 'Smith',
                                                'company_name': 'Acme',
                                                'order_number': 10,
                                                'contact_methods': [{
                                                    'id': 1,
                                                    'destination': '+15145550000',
                                                    'destination_type': 'office_phone' }]
                                              }))
        expected_response = json.dumps({ 'email': 'john.smith@example.com',
                                         'id': 456,
                                         'first_name': '',
                                         'last_name': 'Smith',
                                         'company_name': 'Acme',
                                         'order_number': 10,
                                         'created_at': '2016-04-19T16:26:18.277Z',
                                         'updated_at': '2017-09-07T19:33:51.192Z',
                                         'contact_methods': []
                                       })
        self.client.json_client.update_favorite = Mock(return_value=expected_response)
        self.client.delete_favorite_contact_methods(favorite, [1])
        self.assertFalse(favorite.contact_methods)

    def test_delete_favorite_contact_methods_should_fail_when_id_is_missing(self):
        favorite = Favorite(params=json.dumps({ 'email': 'john.smith@example.com',
                                                'id': None,
                                                'last_name': 'Smith',
                                                'company_name': 'Acme',
                                                'order_number': 10,
                                                'contact_methods': [{
                                                    'id': 1,
                                                    'destination': '+15145550000',
                                                    'destination_type': 'office_phone' }]
                                              }))
        with self.assertRaises(SendSecureException) as context:
            self.client.delete_favorite_contact_methods(favorite, [1])
        self.assertIn('Favorite id cannot be null', context.exception.message)

    def test_delete_favorite(self):
        favorite = Favorite(params=json.dumps({ 'email': 'john.smith@example.com',
                                                'id': 456,
                                                'last_name': 'Smith',
                                                'company_name': 'Acme',
                                                'order_number': 10,
                                                'contact_methods': [{
                                                    'id': 1,
                                                    'destination': '+15145550000',
                                                    'destination_type': 'office_phone' }]
                                              }))
        self.client.json_client.delete_favorite = Mock(return_value=None)
        result = self.client.delete_favorite(favorite)
        self.assertFalse(result)

    def test_create_participant(self):
        participant = Participant(params=json.dumps({ 'first_name': 'John',
                                                      'last_name': 'Smith',
                                                      'email': 'john.smith@example.com',
                                                      'guest_options': {
                                                          'company_name': 'Acme',
                                                          'contact_methods': [
                                                            {
                                                              'destination': '+15145550000',
                                                              'destination_type': 'office_phone'},
                                                            { 'destination': '+15145550001',
                                                              'destination_type': 'cell_phone' }
                                                          ]
                                                      }
                                                    }))
        expected_response = json.dumps({ 'id': '7a3c51e00a004917a8f5db807180fcc5',
                                         'first_name': 'John',
                                         'last_name': 'Smith',
                                         'email': 'john.smith@example.com',
                                         'type': 'guest',
                                         'role': 'guest',
                                         'guest_options': {
                                           'company_name': 'Acme',
                                           'locked': False,
                                           'bounced_email': False,
                                           'failed_login_attempts': 0,
                                           'verified': False,
                                           'contact_methods': [
                                             { 'id': 1,
                                               'destination': '+15145550000',
                                               'destination_type': 'office_phone',
                                               'verified': False,
                                               'created_at': '2017-04-28T17:14:55.304Z',
                                               'updated_at': '2017-04-28T17:14:55.304Z' },
                                             { 'id': 2,
                                               'destination': '+15145550001',
                                               'destination_type': 'cell_phone',
                                               'verified': True,
                                               'created_at': '2017-04-28T18:14:55.304Z',
                                               'updated_at': '2017-04-28T18:14:55.304Z' }
                                           ]
                                          }
                                       })
        self.client.json_client.create_participant = Mock(return_value=expected_response)
        self.client.create_participant(self.safebox, participant)
        self.assertEqual(participant.id, '7a3c51e00a004917a8f5db807180fcc5')
        self.assertEqual(participant.type, 'guest')
        self.assertEqual(participant.role, 'guest')
        self.assertEqual(participant.guest_options.failed_login_attempts, 0)
        self.assertEqual(participant.guest_options.contact_methods[0].id, 1)
        self.assertEqual(participant.guest_options.contact_methods[1].id, 2)
        self.assertEqual(len(self.safebox.participants), 2)


    def test_create_participant_should_fail_when_email_is_missing(self):
        participant = Participant(params=json.dumps({ 'first_name': 'John',
                                                      'last_name': 'Smith',
                                                      'email': None,
                                                      'guest_options': {
                                                          'company_name': 'Acme',
                                                          'contact_methods': [
                                                            {
                                                              'destination': '+15145550000',
                                                              'destination_type': 'office_phone'},
                                                            { 'destination': '+15145550001',
                                                              'destination_type': 'cell_phone' }
                                                          ]
                                                      }
                                                    }))
        with self.assertRaises(SendSecureException) as context:
            self.client.create_participant(self.safebox, participant)
        self.assertIn('Participant email cannot be null', context.exception.message)

    def test_create_participant_should_fail_when_safebox_GUID_is_missing(self):
        participant = Participant(params=json.dumps({ 'first_name': 'John',
                                                      'last_name': 'Smith',
                                                      'email': None,
                                                      'guest_options': {
                                                          'company_name': 'Acme',
                                                          'contact_methods': [
                                                            {
                                                              'destination': '+15145550000',
                                                              'destination_type': 'office_phone'},
                                                            { 'destination': '+15145550001',
                                                              'destination_type': 'cell_phone' }
                                                          ]
                                                      }
                                                    }))
        sb = Safebox(params=json.dumps({ 'guid': None }))
        with self.assertRaises(SendSecureException) as context:
            self.client.create_participant(sb, participant)
        self.assertIn('SafeBox GUID cannot be null', context.exception.message)

    def test_update_participant(self):
        participant = Participant(params=json.dumps({ 'id': '7a3c51e00a004917a8f5db807180fcc5',
                                                      'first_name': '',
                                                      'last_name': '',
                                                      'type': 'guest',
                                                      'role': 'guest',
                                                      'email': 'recipient@test.xmedius.com',
                                                      'guest_options': {
                                                          'company_name': 'Acme',
                                                          'locked': True,
                                                          'bounced_email': False,
                                                          'failed_login_attempts': 0,
                                                          'verified': False,
                                                          'contact_methods': [
                                                              { 'id': 1,
                                                                'destination': '+15145550000',
                                                                'destination_type': 'cell_phone',
                                                                'verified': False,
                                                                'created_at': '2017-04-27T17:14:55.304Z',
                                                                'updated_at': '2017-04-28T17:14:55.304Z'
                                                              }
                                                          ]
                                                      }
                                                    }))
        expected_response = json.dumps({ 'first_name': 'John',
                                         'last_name': 'Smith',
                                         'email': 'recipient@test.xmedius.com',
                                         'type': 'guest',
                                         'role': 'guest',
                                         'guest_options': {
                                           'company_name': 'Acme',
                                           'locked': True,
                                           'bounced_email': False,
                                           'failed_login_attempts': 0,
                                           'verified': False,
                                           'contact_methods': [{
                                               'id': 1,
                                               'destination': '+15145550000',
                                               'destination_type': 'cell_phone',
                                               'verified': False,
                                               'created_at': '2017-04-27T17:14:55.304Z',
                                               'updated_at': '2017-04-29T17:14:55.304Z' }
                                            ]
                                          }
                                       })
        participant.update_attributes(json.dumps({ 'id': '7a3c51e00a004917a8f5db807180fcc5',
                                                   'first_name': 'John',
                                                   'last_name': 'Smith',
                                                   'guest_options': {
                                                       'locked': True
                                                   }
                                                 }))
        self.client.json_client.update_participant = Mock(return_value=expected_response)
        self.client.update_participant(self.safebox, participant)
        self.assertEqual(participant.first_name, 'John')
        self.assertEqual(participant.last_name, 'Smith')
        self.assertTrue(participant.guest_options.locked)

    def test_update_participant_should_fail_when_id_is_missing(self):
        participant = Participant(params=json.dumps({ 'id': None,
                                                      'first_name': '',
                                                      'last_name': '',
                                                      'type': 'guest',
                                                      'role': 'guest',
                                                      'email': 'recipient@test.xmedius.com',
                                                      'guest_options': {
                                                          'company_name': 'Acme',
                                                          'locked': True,
                                                          'bounced_email': False,
                                                          'failed_login_attempts': 0,
                                                          'verified': False,
                                                          'contact_methods': [
                                                              { 'id': 1,
                                                                'destination': '+15145550000',
                                                                'destination_type': 'cell_phone',
                                                                'verified': False,
                                                                'created_at': '2017-04-27T17:14:55.304Z',
                                                                'updated_at': '2017-04-28T17:14:55.304Z'
                                                              }
                                                          ]
                                                      }
                                                    }))
        with self.assertRaises(SendSecureException) as context:
            self.client.update_participant(self.safebox, participant)
        self.assertIn('Participant id cannot be null', context.exception.message)

    def test_update_participant_should_fail_when_safebox_GUID_is_missing(self):
        participant = Participant(params=json.dumps({ 'id': '7a3c51e00a004917a8f5db807180fcc5',
                                                      'first_name': '',
                                                      'last_name': '',
                                                      'type': 'guest',
                                                      'role': 'guest',
                                                      'email': 'recipient@test.xmedius.com',
                                                      'guest_options': {
                                                          'company_name': 'Acme',
                                                          'locked': True,
                                                          'bounced_email': False,
                                                          'failed_login_attempts': 0,
                                                          'verified': False,
                                                          'contact_methods': [
                                                              { 'id': 1,
                                                                'destination': '+15145550000',
                                                                'destination_type': 'cell_phone',
                                                                'verified': False,
                                                                'created_at': '2017-04-27T17:14:55.304Z',
                                                                'updated_at': '2017-04-28T17:14:55.304Z'
                                                              }
                                                          ]
                                                      }
                                                    }))
        sb = Safebox(params=json.dumps({ 'guid': None }))
        with self.assertRaises(SendSecureException) as context:
            self.client.update_participant(sb, participant)
        self.assertIn('SafeBox GUID cannot be null', context.exception.message)

    def test_delete_participant_contact_methods(self):
        participant = Participant(params=json.dumps({ 'id': '7a3c51e00a004917a8f5db807180fcc5',
                                                      'first_name': '',
                                                      'last_name': '',
                                                      'type': 'guest',
                                                      'role': 'guest',
                                                      'email': 'recipient@test.xmedius.com',
                                                      'guest_options': {
                                                          'company_name': 'Acme',
                                                          'locked': True,
                                                          'bounced_email': False,
                                                          'failed_login_attempts': 0,
                                                          'verified': False,
                                                          'contact_methods': [
                                                              { 'id': 1,
                                                                'destination': '+15145550000',
                                                                'destination_type': 'cell_phone',
                                                                'verified': False,
                                                                'created_at': '2017-04-27T17:14:55.304Z',
                                                                'updated_at': '2017-04-28T17:14:55.304Z'
                                                              }
                                                          ]
                                                      }
                                                    }))
        expected_response = json.dumps({ 'first_name': 'John',
                                         'last_name': 'Smith',
                                         'email': 'recipient@test.xmedius.com',
                                         'type': 'guest',
                                         'role': 'guest',
                                         'guest_options': {
                                           'company_name': 'Acme',
                                           'locked': True,
                                           'bounced_email': False,
                                           'failed_login_attempts': 0,
                                           'verified': False,
                                           'contact_methods': []
                                          }
                                       })
        self.client.json_client.update_participant = Mock(return_value=expected_response)
        self.client.delete_participant_contact_methods(self.safebox, participant, [1])
        self.assertFalse(participant.guest_options.contact_methods)

    def test_delete_participant_contact_methods_should_fail_when_id_is_missing(self):
        participant = Participant(params=json.dumps({ 'id': None,
                                                      'first_name': '',
                                                      'last_name': '',
                                                      'type': 'guest',
                                                      'role': 'guest',
                                                      'email': 'recipient@test.xmedius.com',
                                                      'guest_options': {
                                                          'company_name': 'Acme',
                                                          'locked': True,
                                                          'bounced_email': False,
                                                          'failed_login_attempts': 0,
                                                          'verified': False,
                                                          'contact_methods': [
                                                              { 'id': 1,
                                                                'destination': '+15145550000',
                                                                'destination_type': 'cell_phone',
                                                                'verified': False,
                                                                'created_at': '2017-04-27T17:14:55.304Z',
                                                                'updated_at': '2017-04-28T17:14:55.304Z'
                                                              }
                                                          ]
                                                      }
                                                    }))
        with self.assertRaises(SendSecureException) as context:
            self.client.delete_participant_contact_methods(self.safebox, participant, [1])
        self.assertIn('Participant id cannot be null', context.exception.message)

    def test_delete_participant_contact_methods_should_fail_when_safebox_GUID_is_missing(self):
        participant = Participant(params=json.dumps({ 'id': '7a3c51e00a004917a8f5db807180fcc5',
                                                      'first_name': '',
                                                      'last_name': '',
                                                      'type': 'guest',
                                                      'role': 'guest',
                                                      'email': 'recipient@test.xmedius.com',
                                                      'guest_options': {
                                                          'company_name': 'Acme',
                                                          'locked': True,
                                                          'bounced_email': False,
                                                          'failed_login_attempts': 0,
                                                          'verified': False,
                                                          'contact_methods': [
                                                              { 'id': 1,
                                                                'destination': '+15145550000',
                                                                'destination_type': 'cell_phone',
                                                                'verified': False,
                                                                'created_at': '2017-04-27T17:14:55.304Z',
                                                                'updated_at': '2017-04-28T17:14:55.304Z'
                                                              }
                                                          ]
                                                      }
                                                    }))
        sb = Safebox(params=json.dumps({ 'guid': None }))
        with self.assertRaises(SendSecureException) as context:
            self.client.delete_participant_contact_methods(sb, participant, [1])
        self.assertIn('SafeBox GUID cannot be null', context.exception.message)

    def test_search_recipient(self):
        expected_response = json.dumps({ 'results': [
                                            { 'id': 1,
                                              'type': 'favorite',
                                              'first_name': 'John',
                                              'last_name': 'Doe',
                                              'email': 'john@xmedius.com',
                                              'company_name': ''
                                            },
                                            {
                                              'id': 4,
                                              'type': 'favorite',
                                              'first_name': '',
                                              'last_name': '',
                                              'email': 'john@xmedius.com',
                                              'company_name': ''
                                            },
                                            {
                                              'id': 3,
                                              'type': 'user',
                                              'first_name': '',
                                              'last_name': 'john',
                                              'email': 'john.doe@sagemcom.com',
                                              'company_name': ''
                                            }
                                        ]
                                       })
        self.client.json_client.search_recipient = Mock(return_value=expected_response)
        result = self.client.search_recipient('john')
        self.assertEqual(len(result['results']), 3)

    def test_reply(self):
        reply = Reply({'message': 'Reply message'})
        attachment = Attachment({'source': 'simple.pdf', 'content_type': 'application/pdf'})
        reply.attachments.append(attachment)
        expected_response = json.dumps({ 'result': True, 'message': 'SafeBox successfully updated.' })
        new_file_response = json.dumps({ 'temporary_document_guid': '1c820789a50747df8746aa5d71922a3f',
                                         'upload_url': 'http://upload_url/' })
        upload_file_response = json.dumps({ 'temporary_document': {
                                                'document_guid': '65f53ec1282c454fa98439dbda134093'
                                            }})
        self.client.json_client.new_file = Mock(return_value=new_file_response)
        self.client.json_client.upload_file = Mock(return_value=upload_file_response)
        self.client.json_client.reply = Mock(return_value=expected_response)
        result = self.client.reply(self.safebox, reply)
        self.assertTrue(result['result'])
        self.assertEqual(result['message'], 'SafeBox successfully updated.')

    def test_reply_should_fail_when_safebox_GUID_is_missing(self):
        reply = Reply({'message': 'Reply message'})
        sb = Safebox(params=json.dumps({ 'guid': None }))
        with self.assertRaises(SendSecureException) as context:
            self.client.reply(sb, reply)
        self.assertIn('SafeBox GUID cannot be null', context.exception.message)

    def test_add_time(self):
        expected_response = json.dumps({ 'result': True,
                                         'message': 'SafeBox duration successfully extended.',
                                         'new_expiration': '2016-15-06T05:38:09.951Z' })
        self.client.json_client.add_time = Mock(return_value=expected_response)
        result = self.client.add_time(self.safebox, 3, SecurityProfile.TimeUnit.HOURS)
        self.assertTrue(result['result'])
        self.assertEqual(result['message'], 'SafeBox duration successfully extended.')
        self.assertEqual(result['new_expiration'], '2016-15-06T05:38:09.951Z')

    def test_add_time_should_fail_when_safebox_GUID_is_missing(self):
        sb = Safebox(params=json.dumps({ 'guid': None }))
        with self.assertRaises(SendSecureException) as context:
            self.client.add_time(sb, 3, SecurityProfile.TimeUnit.HOURS)
        self.assertIn('SafeBox GUID cannot be null', context.exception.message)

    def test_close_safebox(self):
        expected_response = json.dumps({ 'result': True,
                                         'message': 'SafeBox successfully closed.' })
        self.client.json_client.close_safebox = Mock(return_value=expected_response)
        result = self.client.close_safebox(self.safebox)
        self.assertTrue(result['result'])
        self.assertTrue(result['message'], 'SafeBox successfully closed.')

    def test_close_safebox_should_fail_when_safebox_GUID_is_missing(self):
        sb = Safebox(params=json.dumps({ 'guid': None }))
        with self.assertRaises(SendSecureException) as context:
            self.client.close_safebox(sb)
        self.assertIn('SafeBox GUID cannot be null', context.exception.message)

    def test_delete_safebox_content(self):
        expected_response = json.dumps({ 'result': True,
                                         'message': 'SafeBox content successfully deleted.' })
        self.client.json_client.delete_safebox_content = Mock(return_value=expected_response)
        result = self.client.delete_safebox_content(self.safebox)
        self.assertTrue(result['result'])
        self.assertEqual(result['message'], 'SafeBox content successfully deleted.')

    def test_delete_safebox_content_should_fail_when_safebox_GUID_is_missing(self):
        sb = Safebox(params=json.dumps({ 'guid': None }))
        with self.assertRaises(SendSecureException) as context:
            self.client.delete_safebox_content(sb)
        self.assertIn('SafeBox GUID cannot be null', context.exception.message)

    def test_mark_as_read(self):
        expected_response = json.dumps({ 'result': True })
        self.client.json_client.mark_as_read = Mock(return_value=expected_response)
        result = self.client.mark_as_read(self.safebox)
        self.assertTrue(result['result'])

    def test_mark_as_read_should_fail_when_safebox_GUID_is_empty(self):
        sb = Safebox(params=json.dumps({ 'guid': None }))
        with self.assertRaises(SendSecureException) as context:
            self.client.mark_as_read(sb)
        self.assertIn('SafeBox GUID cannot be null', context.exception.message)

    def test_mark_as_unread(self):
        expected_response = json.dumps({ 'result': True })
        self.client.json_client.mark_as_unread = Mock(return_value=expected_response)
        result = self.client.mark_as_unread(self.safebox)
        self.assertTrue(result['result'])

    def test_mark_as_unread_should_fail_when_safebox_GUID_is_empty(self):
        sb = Safebox(params=json.dumps({ 'guid': None }))
        with self.assertRaises(SendSecureException) as context:
            self.client.mark_as_unread(sb)
        self.assertIn('SafeBox GUID cannot be null', context.exception.message)

    def test_mark_as_read_message(self):
        message = Message(json.dumps({ 'id': 145926,
                                       'note': 'Lorem Ipsum...',
                                       'note_size': 148,
                                       'read': True,
                                       'author_id': '3',
                                       'author_type': 'guest',
                                       'created_at': '2017-04-05T14:49:35.198Z',
                                       'documents': []
                                     }))
        expected_response = json.dumps({ 'result': True })
        self.client.json_client.mark_as_read_message = Mock(return_value=expected_response)
        result = self.client.mark_as_read_message(self.safebox, message)

    def test_mark_as_read_message_should_fail_when_safebox_GUID_is_empty(self):
        message = Message(json.dumps({ 'id': 145926,
                                       'note': 'Lorem Ipsum...',
                                       'note_size': 148,
                                       'read': True,
                                       'author_id': '3',
                                       'author_type': 'guest',
                                       'created_at': '2017-04-05T14:49:35.198Z',
                                       'documents': []
                                     }))
        sb = Safebox(params=json.dumps({ 'guid': None }))
        with self.assertRaises(SendSecureException) as context:
            self.client.mark_as_read_message(sb, message)
        self.assertIn('SafeBox GUID cannot be null', context.exception.message)

    def test_mark_as_unread_message(self):
        message = Message(json.dumps({ 'id': 145926,
                                       'note': 'Lorem Ipsum...',
                                       'note_size': 148,
                                       'read': True,
                                       'author_id': '3',
                                       'author_type': 'guest',
                                       'created_at': '2017-04-05T14:49:35.198Z',
                                       'documents': []
                                     }))
        expected_response = json.dumps({ 'result': True })
        self.client.json_client.mark_as_unread_message = Mock(return_value=expected_response)
        result = self.client.mark_as_unread_message(self.safebox, message)

    def test_mark_as_unread_message_should_fail_when_safebox_GUID_is_empty(self):
        message = Message(json.dumps({ 'id': 145926,
                                       'note': 'Lorem Ipsum...',
                                       'note_size': 148,
                                       'read': True,
                                       'author_id': '3',
                                       'author_type': 'guest',
                                       'created_at': '2017-04-05T14:49:35.198Z',
                                       'documents': []
                                     }))
        sb = Safebox(params=json.dumps({ 'guid': None }))
        with self.assertRaises(SendSecureException) as context:
            self.client.mark_as_unread_message(sb, message)
        self.assertIn('SafeBox GUID cannot be null', context.exception.message)

    def test_get_file_url(self):
        expected_response = json.dumps({ 'url': 'https://fileserver.integration.xmedius.com/xmss/DteeDmb-2zfN5WtCbgpJfSENaNjvbHi_nt' })
        document = Attachment({'source': 'test.pdf', 'content_type': 'application/pdf'})
        document.guid = '2w1eg4q4ve2654tyjyu45ujyoiow54euqn'
        self.client.json_client.get_file_url = Mock(return_value=expected_response)
        result = self.client.get_file_url(self.safebox, document)
        self.assertEqual(result, 'https://fileserver.integration.xmedius.com/xmss/DteeDmb-2zfN5WtCbgpJfSENaNjvbHi_nt')

    def test_get_file_url_should_fail_when_safebox_GUID_is_missing(self):
        document = Attachment({'source': 'test.pdf', 'content_type': 'application/pdf'})
        document.guid = '2w1eg4q4ve2654tyjyu45ujyoiow54euqn'
        sb = Safebox(params=json.dumps({ 'guid': None }))
        with self.assertRaises(SendSecureException) as context:
            self.client.get_file_url(sb, document)
        self.assertIn('SafeBox GUID cannot be null', context.exception.message)

    def test_get_file_url_should_fail_when_document_GUID_is_missing(self):
        document = Attachment({'source': 'test.pdf', 'content_type': 'application/pdf'})
        sb = Safebox(params=json.dumps({ 'guid': None }))
        with self.assertRaises(SendSecureException) as context:
            self.client.get_file_url(self.safebox, document)
        self.assertIn('Document GUID cannot be null', context.exception.message)

    def test_get_audit_record_url(self):
        expected_response = json.dumps({ 'url': 'https://fileserver.integration.xmedius.com/xmss/DteeDmb-WJEHEF4EWF75TGaNjvbHi_nt' })
        self.client.json_client.get_audit_record_url = Mock(return_value=expected_response)
        result = self.client.get_audit_record_url(self.safebox)
        self.assertEqual(result, 'https://fileserver.integration.xmedius.com/xmss/DteeDmb-WJEHEF4EWF75TGaNjvbHi_nt')

    def test_get_audit_record_url_should_fail_when_safebox_GUID_is_missing(self):
        sb = Safebox(params=json.dumps({ 'guid': None }))
        with self.assertRaises(SendSecureException) as context:
            self.client.get_audit_record_url(sb)
        self.assertIn('SafeBox GUID cannot be null', context.exception.message)

    def test_get_safeboxes(self):
        expected_response = json.dumps({ 'count': 2,
                                         'previous_page_url': None,
                                         'next_page_url': 'api/v2/safeboxes?status=unread&search=test&page=2',
                                         'safeboxes': [
                                             { 'safebox': {
                                                   'guid': '73af62f766ee459e81f46e4f533085a4',
                                                   'user_id': 1,
                                                   'enterprise_id': 1,
                                                   'subject': 'Donec rutrum congue leo eget malesuada. ',
                                                   'notification_language': 'de',
                                                   'status': 'in_progress',
                                                   'security_profile_name': 'All Contact Method Allowed!',
                                                   'unread_count': 0,
                                                   'double_encryption_status': 'disabled',
                                                   'audit_record_pdf': None,
                                                   'secure_link': None,
                                                   'secure_link_title': None,
                                                   'email_notification_enabled': True,
                                                   'created_at': '2017-05-24T14:45:35.062Z',
                                                   'updated_at': '2017-05-24T14:45:35.589Z',
                                                   'assigned_at': '2017-05-24T14:45:35.040Z',
                                                   'latest_activity': '2017-05-24T14:45:35.544Z',
                                                   'expiration': '2017-05-31T14:45:35.038Z',
                                                   'closed_at': None,
                                                   'content_deleted_at': None
                                            }},
                                             { 'safebox': {
                                                       'guid': '73af62f7ruwehdfjwweg85eore853085a4',
                                                       'user_id': 1,
                                                       'enterprise_id': 1,
                                                       'subject': 'Donec rutrum congue leo eget malesuada. ',
                                                       'notification_language': 'de',
                                                       'status': 'in_progress',
                                                       'security_profile_name': 'All Contact Method Allowed!',
                                                       'unread_count': 0,
                                                       'double_encryption_status': 'disabled',
                                                       'audit_record_pdf': None,
                                                       'secure_link': None,
                                                       'secure_link_title': None,
                                                       'email_notification_enabled': True,
                                                       'created_at': '2017-05-24T14:45:35.062Z',
                                                       'updated_at': '2017-05-24T14:45:35.589Z',
                                                       'assigned_at': '2017-05-24T14:45:35.040Z',
                                                       'latest_activity': '2017-05-24T14:45:35.544Z',
                                                       'expiration': '2017-05-31T14:45:35.038Z',
                                                       'closed_at': None,
                                                       'content_deleted_at': None
                                            }}
                                         ] })
        self.client.json_client.get_safeboxes = Mock(return_value=expected_response)
        result = self.client.get_safeboxes()
        self.assertEqual(len(result['safeboxes']), 2)
        self.assertIsInstance(result['safeboxes'][0], Safebox)
        self.assertIsInstance(result['safeboxes'][1], Safebox)

    def test_get_safebox(self):
        expected_response = json.dumps({ 'count': 2,
                                         'previous_page_url': None,
                                         'next_page_url': 'api/v2/safeboxes?status=unread&search=test&page=2',
                                         'safeboxes': [
                                             { 'safebox': {
                                                   'guid': '73af62f766ee459e81f46e4f533085a4',
                                                   'user_id': 1,
                                                   'enterprise_id': 1,
                                                   'subject': 'Donec rutrum congue leo eget malesuada. ',
                                                   'notification_language': 'de',
                                                   'status': 'in_progress',
                                                   'security_profile_name': 'All Contact Method Allowed!',
                                                   'unread_count': 0,
                                                   'double_encryption_status': 'disabled',
                                                   'audit_record_pdf': None,
                                                   'secure_link': None,
                                                   'secure_link_title': None,
                                                   'email_notification_enabled': True,
                                                   'created_at': '2017-05-24T14:45:35.062Z',
                                                   'updated_at': '2017-05-24T14:45:35.589Z',
                                                   'assigned_at': '2017-05-24T14:45:35.040Z',
                                                   'latest_activity': '2017-05-24T14:45:35.544Z',
                                                   'expiration': '2017-05-31T14:45:35.038Z',
                                                   'closed_at': None,
                                                   'content_deleted_at': None
                                            }},
                                             { 'safebox': {
                                                       'guid': 'f5wef7we5fwe5wef455533085a4',
                                                       'user_id': 1,
                                                       'enterprise_id': 1,
                                                       'subject': 'Donec rutrum congue leo eget malesuada. ',
                                                       'notification_language': 'de',
                                                       'status': 'in_progress',
                                                       'security_profile_name': 'All Contact Method Allowed!',
                                                       'unread_count': 0,
                                                       'double_encryption_status': 'disabled',
                                                       'audit_record_pdf': None,
                                                       'secure_link': None,
                                                       'secure_link_title': None,
                                                       'email_notification_enabled': True,
                                                       'created_at': '2017-05-24T14:45:35.062Z',
                                                       'updated_at': '2017-05-24T14:45:35.589Z',
                                                       'assigned_at': '2017-05-24T14:45:35.040Z',
                                                       'latest_activity': '2017-05-24T14:45:35.544Z',
                                                       'expiration': '2017-05-31T14:45:35.038Z',
                                                       'closed_at': None,
                                                       'content_deleted_at': None
                                            }}
                                         ] })
        self.client.json_client.get_safeboxes = Mock(return_value=expected_response)
        result = self.client.get_safebox('f5wef7we5fwe5wef455533085a4')
        self.assertIsInstance(result, Safebox)
        self.assertEqual(result.guid, 'f5wef7we5fwe5wef455533085a4')

    def test_get_safebox_info(self):
        sb = Safebox(params=json.dumps({'guid': '1c820789a50747df8746aa5d71922a3f','user_email': 'user@acme.com'}))
        expected_response = json.dumps({ 'safebox': {
                                             'guid': '1c820789a50747df8746aa5d71922a3f',
                                             'user_id': 1,
                                             'enterprise_id': 1,
                                             'participants': [
                                                 { 'id': '7a3c51e00a004917a8f5db807180fcc5',
                                                   'guest_options': {},
                                                   'message_read_count': 0,
                                                   'message_total_count': 1
                                                 },
                                                 { 'id': '1',
                                                   'first_name': 'Jane',
                                                   'last_name': 'Doe',
                                                   'email': 'jane.doe@example.com',
                                                   'type': 'user',
                                                   'role': 'owner',
                                                   'message_read_count': 0,
                                                   'message_total_count': 1
                                                 }],
                                             'security_options': {
                                                 'security_code_length': 4
                                             },
                                             'messages': [
                                                 { 'note': 'Lorem Ipsum...',
                                                   'note_size': 123,
                                                   'documents': [] }
                                             ],
                                             'download_activity': {
                                                 'guests': [
                                                     { 'id': '42220c777c30486e80cd3bbfa7f8e82f',
                                                       'documents': []
                                                     }
                                                 ],
                                                 'owner': {
                                                     'id': 1,
                                                     'documents': []
                                                 }
                                             },
                                             'event_history': [
                                                 { 'type': 'safebox_created_owner',
                                                   'date': '2017-03-30T18:09:05.966Z',
                                                   'metadata': {},
                                                   'message': 'SafeBox created by user@example.com with 0 attachment(s) from 0.0.0.0 for john.smith@example.com' }
                                             ]}
                                       })
        self.client.json_client.get_safebox_info = Mock(return_value=expected_response)
        self.client.get_safebox_info(sb)
        self.assertEqual(len(sb.participants), 2)
        self.assertTrue(sb.security_options)
        self.assertEqual(len(sb.messages), 1)
        self.assertEqual(len(sb.download_activity.guests), 1)
        self.assertTrue(sb.download_activity.owner)
        self.assertEqual(len(sb.event_history), 1)

    def test_get_safebox_info_should_fail_when_safebox_GUID_is_missing(self):
        sb = Safebox(params=json.dumps({ 'guid': None }))
        with self.assertRaises(SendSecureException) as context:
            self.client.get_safebox_info(sb)
        self.assertIn('SafeBox GUID cannot be null', context.exception.message)

    def test_get_safebox_participants(self):
        expected_response = json.dumps({ 'participants': [{
                                            'id': '7a3c51e00a004917a8f5db807180fcc5',
                                            'first_name': '',
                                            'last_name': '',
                                            'email': 'john.smith@example.com',
                                            'type': 'guest',
                                            'role': 'guest',
                                            'guest_options': {
                                              'company_name': '',
                                              'locked': False,
                                              'bounced_email': False,
                                              'failed_login_attempts': 0,
                                              'verified': False,
                                              'contact_methods': [{
                                                  'id': 35016,
                                                  'destination': '+15145550000',
                                                  'destination_type': 'cell_phone',
                                                  'verified': False,
                                                  'created_at': '2017-05-24T14:45:35.453Z',
                                                  'updated_at': '2017-05-24T14:45:35.453Z' }]
                                            }},
                                          {
                                            'id': 34208,
                                            'first_name': 'Jane',
                                            'last_name': 'Doe',
                                            'email': 'jane.doe@example.com',
                                            'type': 'user',
                                            'role': 'owner' }]
                                       })
        self.client.json_client.get_safebox_participants = Mock(return_value=expected_response)
        result = self.client.get_safebox_participants(self.safebox)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], Participant)
        self.assertEqual(result[0].id, '7a3c51e00a004917a8f5db807180fcc5')
        self.assertIsInstance(result[1], Participant)
        self.assertEqual(result[1].id, 34208)

    def test_get_safebox_participants_should_fail_when_safebox_GUID_is_missing(self):
        sb = Safebox(params=json.dumps({ 'guid': None }))
        with self.assertRaises(SendSecureException) as context:
            self.client.get_safebox_participants(sb)
        self.assertIn('SafeBox GUID cannot be null', context.exception.message)

    def test_get_safebox_messages(self):
        expected_response = json.dumps({ 'messages': [{
                                             'note': 'Lorem Ipsum...',
                                             'note_size': 148,
                                             'read': True,
                                             'author_id': '3',
                                             'author_type': 'guest',
                                             'created_at': '2017-04-05T14:49:35.198Z',
                                             'documents': [
                                                {
                                                 'id': '5a3df276aaa24e43af5aca9b2204a535',
                                                 'name': 'Axient-soapui-project.xml',
                                                 'sha': '724ae04430315c60ca17f4dbee775a37f5b18c05aee99c9c',
                                                 'size': 129961,
                                                 'url': 'https://sendsecure.xmedius.com/api/v2/safeboxes/b4d898ada15f42f293e31905c514607f/documents/5a3df276aaa24e43af5aca9b2204a535/url'
                                                }] }]
                                       })
        self.client.json_client.get_safebox_messages = Mock(return_value=expected_response)
        result = self.client.get_safebox_messages(self.safebox)
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], Message)
        self.assertEqual(len(result[0].documents), 1)
        self.assertEqual(result[0].documents[0].id, '5a3df276aaa24e43af5aca9b2204a535')

    def test_get_safebox_messages_should_fail_when_safebox_GUID_is_missing(self):
        sb = Safebox(params=json.dumps({ 'guid': None }))
        with self.assertRaises(SendSecureException) as context:
            self.client.get_safebox_messages(sb)
        self.assertIn('SafeBox GUID cannot be null', context.exception.message)

    def test_get_safebox_security_options(self):
        expected_response = json.dumps({ 'security_options': {
                                             'security_code_length': 4,
                                             'allowed_login_attempts': 3,
                                             'allow_remember_me': True,
                                             'allow_sms': True,
                                             'allow_voice': True,
                                             'allow_email': False,
                                             'reply_enabled': True,
                                             'group_replies': False,
                                             'code_time_limit': 5,
                                             'encrypt_message': True,
                                             'two_factor_required': True,
                                             'auto_extend_value': 3,
                                             'auto_extend_unit': 'days',
                                             'retention_period_type': 'do_not_discard',
                                             'retention_period_value': None,
                                             'retention_period_unit': 'hours',
                                             'delete_content_on': None,
                                             'allow_manual_delete': True,
                                             'allow_manual_close': False
                                       }})
        self.client.json_client.get_safebox_security_options = Mock(return_value=expected_response)
        result = self.client.get_safebox_security_options(self.safebox)
        self.assertIsInstance(result, SecurityOptions)
        self.assertEqual(result.security_code_length, 4)

    def test_get_safebox_security_options_should_fail_when_safebox_GUID_is_missing(self):
        sb = Safebox(params=json.dumps({ 'guid': None }))
        with self.assertRaises(SendSecureException) as context:
            self.client.get_safebox_security_options(sb)
        self.assertIn('SafeBox GUID cannot be null', context.exception.message)

    def test_get_safebox_download_activity(self):
        expected_response = json.dumps({ 'download_activity': {
                                             'guests': [
                                                {
                                                 'id': '42220c777c30486e80cd3bbfa7f8e82f',
                                                 'documents': [
                                                    {
                                                     'id': '5a3df276aaa24e43af5aca9b2204a535',
                                                     'downloaded_bytes': 0,
                                                     'download_date': None
                                                    }]
                                                }],
                                             'owner': {
                                               'id': 72,
                                               'documents': [] }
                                        }})
        self.client.json_client.get_safebox_download_activity = Mock(return_value=expected_response)
        result = self.client.get_safebox_download_activity(self.safebox)
        self.assertIsInstance(result, DownloadActivity)
        self.assertEqual(len(result.guests), 1)
        self.assertEqual(len(result.guests[0].documents), 1)
        self.assertEqual(result.owner.id, 72)

    def test_get_safebox_download_activity_should_fail_when_safebox_GUID_is_missing(self):
        sb = Safebox(params=json.dumps({ 'guid': None }))
        with self.assertRaises(SendSecureException) as context:
            self.client.get_safebox_download_activity(sb)
        self.assertIn('SafeBox GUID cannot be null', context.exception.message)

    def test_get_safebox_event_history(self):
        expected_response = json.dumps({ 'event_history': [
                                             { 'type': '42220c777c30486e80cd3bbfa7f8e82f',
                                               'date': [],
                                               'metadata': {},
                                               'message': 'SafeBox created by john.smith@example.com with 0 attachment(s) from 0.0.0.0 for john.smith@example.com' }
                                         ]
                                       })
        self.client.json_client.get_safebox_event_history = Mock(return_value=expected_response)
        result = self.client.get_safebox_event_history(self.safebox)
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], EventHistory)
        self.assertEqual(result[0].type, '42220c777c30486e80cd3bbfa7f8e82f')


    def test_get_safebox_event_history_should_fail_when_safebox_GUID_is_missing(self):
        sb = Safebox(params=json.dumps({ 'guid': None }))
        with self.assertRaises(SendSecureException) as context:
            self.client.get_safebox_event_history(sb)
        self.assertIn('SafeBox GUID cannot be null', context.exception.message)

    def test_get_consent_group_messages_error(self):
        expected_response = json.dumps({ 'consent_message_group': {
                                            'id': 1,
                                            'name': 'Default',
                                            'created_at': '2016-08-29T14:52:26.085Z',
                                            'updated_at': '2016-08-29T14:52:26.085Z',
                                            'consent_messages': [{
                                                'locale': 'en',
                                                'value': 'Lorem ipsum',
                                                'created_at': '2016-08-29T14:52:26.085Z',
                                                'updated_at': '2016-08-29T14:52:26.085Z'
                                            }]}
                                        })
        self.client.json_client.get_consent_group_messages = Mock(return_value=expected_response)
        result = self.client.get_consent_group_messages(1)
        self.assertIsInstance(result, ConsentMessageGroup)
        self.assertEqual(result.id, 1)
        self.assertEqual(result.name, 'Default')
        self.assertEqual(len(result.consent_messages), 1)
        self.assertIsInstance(result.consent_messages[0], ConsentMessage)
        self.assertEqual(result.consent_messages[0].locale, 'en')
        self.assertEqual(result.consent_messages[0].value, 'Lorem ipsum')

if __name__ == '__main__':
    unittest.main()






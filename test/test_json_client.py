import path
from sendsecure import *
import unittest
try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock

class TestJsonClient(unittest.TestCase):
    client = JsonClient({ 'api_token': 'USER|489b3b1f-b411-428e-be5b-2abbace87689',
                          'user_id': '123456',
                          'enterprise_account': 'acme',
                          'endpoint': 'https://awesome.portal' })
    client._get_sendsecure_endpoint = Mock(return_value='https://awesome.sendsecure.portal/')
    safebox_guid = '7a3c51e00a004917a8f5db807180fcc5'

    def test_new_safebox_success(self):
        expected_response = json.dumps({ 'guid': '1234sa4sad87ew87t', 'public_encryption_key': 'key', 'upload_url': 'url'})
        self.client._do_get = Mock(return_value=expected_response)
        result = json.loads(self.client.new_safebox('user@email.com'))
        self.client._do_get.assert_called_once_with('https://awesome.sendsecure.portal/api/v2/safeboxes/new.json?user_email=user@email.com',
                                                    'application/json')
        self.assertEqual(result['guid'], '1234sa4sad87ew87t')
        self.assertEqual(result['public_encryption_key'], 'key')
        self.assertEqual(result['upload_url'], 'url')

    def test_new_safebox_error(self):
        self.client._do_get = Mock(side_effect=SendSecureException(403, 'Access denied', ''))
        with self.assertRaises(SendSecureException) as context:
            result = self.client.new_safebox('user@example.com')
        self.client._do_get.assert_called_once_with('https://awesome.sendsecure.portal/api/v2/safeboxes/new.json?user_email=user@example.com',
                                                    'application/json')
        self.assertEqual(context.exception.code, 403)
        self.assertIn('Access denied', context.exception.message)

    def test_new_file_success(self):
        file_params = json.dumps({ 'temporary_document': { 'document_file_size': 17580 },
                                   'multipart': False,
                                   'public_encryption_key': 'AyOmyAawJXKepb9LuJAOyiJXvk'
                                 })
        expected_response = json.dumps({ 'temporary_document_guid': '1c820789a50747df8746aa5d71922a3f',
                                         'upload_url': 'http://upload_url/' })
        self.client._do_post = Mock(return_value=expected_response)
        result = json.loads(self.client.new_file(self.safebox_guid, file_params))
        self.client._do_post.assert_called_once_with('https://awesome.sendsecure.portal/api/v2/safeboxes/7a3c51e00a004917a8f5db807180fcc5/uploads.json',
                                                     'application/json',
                                                     file_params,
                                                     'application/json')
        self.assertEqual(result['temporary_document_guid'], '1c820789a50747df8746aa5d71922a3f')
        self.assertEqual(result['upload_url'], 'http://upload_url/')

    def test_commit_safebox_success(self):
        safebox_json = json.dumps({
            'safebox': { 'guid': '1c820789a50747df8746aa5d71922a3f',
                         'recipients': [{ 'email': 'recipient@test.xmedius.com',
                                          'contact_methods': [
                                              { 'destination_type': 'cell_phone',
                                                'destination': '+15145550000'
                                              }]
                                        }],
                         'message': 'lorem ipsum...',
                         'security_profile_id': 10,
                         'public_encryption_key': 'AyOmyAawJXKepb9LuJAyCaciv7QBt5Dqoz',
                         'notification_language': ''}})
        expected_response = json.dumps({ 'guid': '1c820789a50747df8746aa5d71922a3f',
                                         'user_id': 3,
                                         'enterprise_id': 1 })
        self.client._do_post = Mock(return_value=expected_response)
        result = json.loads(self.client.commit_safebox(safebox_json))
        self.client._do_post.assert_called_once_with('https://awesome.sendsecure.portal/api/v2/safeboxes.json',
                                                     'application/json',
                                                     safebox_json,
                                                     'application/json')
        self.assertEqual(result['guid'], '1c820789a50747df8746aa5d71922a3f')
        self.assertEqual(result['user_id'], 3)
        self.assertEqual(result['enterprise_id'], 1)

    def test_commit_safebox_error(self):
        safebox_json = json.dumps({
            'safebox': { 'guid': '1c820789a50747df8746aa5d71922a3f',
                         'recipients': [{ 'email': 'recipient@test.xmedius.com',
                                          'contact_methods': [
                                              { 'destination_type': 'cell_phone',
                                                'destination': '+15145550000'
                                              }]
                                        }],
                         'message': 'lorem ipsum...',
                         'security_profile_id': 10,
                         'public_encryption_key': 'AyOmyAawJXKepb9LuJAyCaciv7QBt5Dqoz',
                         'notification_language': ''}})
        expected_error = json.dumps({'error':'Some entered values are incorrect.', 'attributes':{'language':['cannot be blank']}})
        self.client._do_post = Mock(side_effect=SendSecureException(400, expected_error, ''))
        with self.assertRaises(SendSecureException) as context:
            result = self.client.commit_safebox(safebox_json)
        self.client._do_post.assert_called_once_with('https://awesome.sendsecure.portal/api/v2/safeboxes.json',
                                                 'application/json',
                                                 safebox_json,
                                                 'application/json')
        self.assertEqual(context.exception.code, 400)
        self.assertIn(expected_error, context.exception.message)

    def test_get_security_profiles_success(self):
        expected_response = json.dumps({ 'security_profiles': [{ 'id': 5 }, { 'id': 10 }] })
        self.client._do_get = Mock(return_value=expected_response)
        result = json.loads(self.client.get_security_profiles('user@example.com'))
        self.client._do_get.assert_called_once_with('https://awesome.sendsecure.portal/api/v2/enterprises/acme/security_profiles.json?user_email=user@example.com',
                                                     'application/json')
        self.assertEqual(len(result['security_profiles']), 2)


    def test_get_security_profiles_error(self):
        self.client._do_get = Mock(side_effect=SendSecureException(403, 'Access denied', ''))
        with self.assertRaises(SendSecureException) as context:
            result = self.client.get_security_profiles('user@example.com')
        self.client._do_get.assert_called_once_with('https://awesome.sendsecure.portal/api/v2/enterprises/acme/security_profiles.json?user_email=user@example.com',
                                                     'application/json')
        self.assertEqual(context.exception.code, 403)
        self.assertIn('Access denied', context.exception.message)

    def test_get_enterprise_settings_success(self):
        expected_response = json.dumps({ 'created_at': '2016-03-15T19:58:11.588Z',
                                         'updated_at': '2016-09-28T18:32:16.643Z',
                                         'default_security_profile_id': 10 })
        self.client._do_get = Mock(return_value=expected_response)
        result = json.loads(self.client.get_enterprise_settings())
        self.client._do_get.assert_called_once_with('https://awesome.sendsecure.portal/api/v2/enterprises/acme/settings.json',
                                                    'application/json')
        self.assertEqual(result['created_at'], '2016-03-15T19:58:11.588Z')
        self.assertEqual(result['updated_at'], '2016-09-28T18:32:16.643Z')
        self.assertEqual(result['default_security_profile_id'], 10)

    def test_get_enterprise_settings_error(self):
        self.client._do_get = Mock(side_effect=SendSecureException(403, 'Access denied', ''))
        with self.assertRaises(SendSecureException) as context:
            result = self.client.get_enterprise_settings()
        self.client._do_get.assert_called_once_with('https://awesome.sendsecure.portal/api/v2/enterprises/acme/settings.json',
                                                    'application/json')
        self.assertEqual(context.exception.code, 403)
        self.assertIn('Access denied', context.exception.message)

    def test_get_user_settings_success(self):
        expected_response = json.dumps({ 'created_at': '2016-03-15T19:58:11.588Z',
                                         'updated_at': '2016-09-28T18:32:16.643Z',
                                         'default_filter': 'unread' })
        self.client._do_get = Mock(return_value=expected_response)
        result = json.loads(self.client.get_user_settings())
        self.client._do_get.assert_called_once_with('https://awesome.sendsecure.portal/api/v2/enterprises/acme/users/123456/settings.json',
                                                    'application/json')
        self.assertEqual(result['created_at'], '2016-03-15T19:58:11.588Z')
        self.assertEqual(result['updated_at'], '2016-09-28T18:32:16.643Z')
        self.assertEqual(result['default_filter'], 'unread')

    def test_get_user_settings_error(self):
        self.client._do_get = Mock(side_effect=SendSecureException(403, 'Access denied', ''))
        with self.assertRaises(SendSecureException) as context:
            result = self.client.get_user_settings()
        self.client._do_get.assert_called_once_with('https://awesome.sendsecure.portal/api/v2/enterprises/acme/users/123456/settings.json',
                                                    'application/json')
        self.assertEqual(context.exception.code, 403)
        self.assertIn('Access denied', context.exception.message)

    def test_get_favorites_succcess(self):
        expected_response = json.dumps({ 'favorites': [
                                            { 'email': 'john.smith@example.com',
                                              'id': 456 },
                                            { 'email': 'jane.doe@example.com',
                                              'id': 789 } ] })
        self.client._do_get = Mock(return_value=expected_response)
        result = json.loads(self.client.get_favorites())
        self.client._do_get.assert_called_once_with('https://awesome.sendsecure.portal/api/v2/enterprises/acme/users/123456/favorites.json',
                                                    'application/json')
        self.assertEqual(len(result['favorites']), 2)
        self.assertEqual(result['favorites'][0]['id'], 456)
        self.assertEqual(result['favorites'][0]['email'], 'john.smith@example.com')
        self.assertEqual(result['favorites'][1]['id'], 789)
        self.assertEqual(result['favorites'][1]['email'], 'jane.doe@example.com')

    def test_get_favorites_error(self):
        self.client._do_get = Mock(side_effect=SendSecureException(403, 'Access denied', ''))
        with self.assertRaises(SendSecureException) as context:
            result = self.client.get_favorites()
        self.client._do_get.assert_called_once_with('https://awesome.sendsecure.portal/api/v2/enterprises/acme/users/123456/favorites.json',
                                                    'application/json')
        self.assertEqual(context.exception.code, 403)
        self.assertIn('Access denied', context.exception.message)

    def test_create_favorite_success(self):
        favorite_json = json.dumps({ 'favorite': {
                                         'first_name': 'John',
                                         'last_name': 'Smith',
                                         'email': 'john.smith@example.com',
                                         'company_name': 'Acme',
                                         'contact_methods':[
                                             { 'destination': '+15145550000',
                                               'destination_type': 'office_phone' },
                                             { 'destination': '+15145550001',
                                               'destination_type': 'cell_phone' }]}
                                   })
        expected_response = json.dumps({ 'id': 456,
                                         'created_at': '2017-04-28T17:18:30.850Z',
                                         'contact_methods': [
                                             { 'id': 1,
                                               'created_at': '2017-04-28T17:14:55.304Z' },
                                             { 'id': 2,
                                               'created_at': '2017-04-28T18:14:55.304Z' }]
                                       })
        self.client._do_post = Mock(return_value=expected_response)
        result = json.loads(self.client.create_favorite(favorite_json))
        self.client._do_post.assert_called_once_with('https://awesome.sendsecure.portal/api/v2/enterprises/acme/users/123456/favorites.json',
                                                    'application/json',
                                                    favorite_json,
                                                    'application/json')
        self.assertEqual(result['id'], 456)
        self.assertEqual(result['created_at'], '2017-04-28T17:18:30.850Z')
        self.assertEqual(len(result['contact_methods']), 2)
        self.assertEqual(result['contact_methods'][0]['id'], 1)
        self.assertEqual(result['contact_methods'][0]['created_at'], '2017-04-28T17:14:55.304Z')
        self.assertEqual(result['contact_methods'][1]['id'], 2)
        self.assertEqual(result['contact_methods'][1]['created_at'], '2017-04-28T18:14:55.304Z')

    def test_create_favorite_error(self):
        favorite_json = json.dumps({ 'favorite': {
                                         'first_name': 'John',
                                         'last_name': 'Smith',
                                         'email': '',
                                         'company_name': 'Acme',
                                         'contact_methods':[
                                             { 'destination': '+15145550000',
                                               'destination_type': 'office_phone' },
                                             { 'destination': '+15145550001',
                                               'destination_type': 'cell_phone' }]}
                                   })
        expected_error = json.dumps({'error':'Some entered values are incorrect.', 'attributes':{'email':['cannot be blank']}})
        self.client._do_post = Mock(side_effect=SendSecureException(400, expected_error, ''))
        with self.assertRaises(SendSecureException) as context:
            result = self.client.create_favorite(favorite_json)
        self.client._do_post.assert_called_once_with('https://awesome.sendsecure.portal/api/v2/enterprises/acme/users/123456/favorites.json',
                                                    'application/json',
                                                    favorite_json,
                                                    'application/json')
        self.assertEqual(context.exception.code, 400)
        self.assertIn(expected_error, context.exception.message)

    def test_update_favorite_success(self):
        favorite_json = json.dumps({ 'favorite': {
                                         'id': 456,
                                         'first_name': 'John',
                                         'last_name': 'Smith',
                                         'email': 'john.smith@example.com',
                                         'order_number': 10,
                                         'company_name': 'Acme',
                                         'contact_methods':[
                                             { 'id': 1,
                                               'destination': '+15145550000',
                                               'destination_type': 'office_phone' },
                                             { 'destination': '+15145550001',
                                               'destination_type': 'cell_phone' }]}
                                    })
        expected_response = json.dumps({ 'id': 456,
                                         'created_at': '2017-04-28T17:18:30.850Z',
                                         'updated_at': '2017-04-28T17:20:54.320Z',
                                         'contact_methods': [
                                             { 'id': 1,
                                               'created_at': '2017-04-28T17:14:55.304Z',
                                               'updated_at': '2017-04-28T17:20:54.320Z' },
                                             { 'id': 2,
                                               'created_at': '2017-04-28T18:14:55.304Z',
                                               'updated_at': '2017-04-28T17:20:54.320Z' }]
                                       })
        self.client._do_patch = Mock(return_value=expected_response)
        result = json.loads(self.client.update_favorite(456, favorite_json))
        self.client._do_patch.assert_called_once_with('https://awesome.sendsecure.portal/api/v2/enterprises/acme/users/123456/favorites/456.json',
                                                    'application/json',
                                                    favorite_json,
                                                    'application/json')
        self.assertEqual(result['id'], 456)
        self.assertEqual(result['updated_at'], '2017-04-28T17:20:54.320Z')
        self.assertEqual(len(result['contact_methods']), 2)
        self.assertEqual(result['contact_methods'][0]['id'], 1)
        self.assertEqual(result['contact_methods'][0]['updated_at'], '2017-04-28T17:20:54.320Z')
        self.assertEqual(result['contact_methods'][1]['id'], 2)
        self.assertEqual(result['contact_methods'][1]['created_at'], '2017-04-28T18:14:55.304Z')

    def test_update_favorite_error(self):
        favorite_json = json.dumps({ 'favorite': {
                                         'id': 456,
                                         'first_name': 'John',
                                         'last_name': 'Smith',
                                         'email': '',
                                         'order_number': 10,
                                         'company_name': 'Acme',
                                         'contact_methods':[
                                             { 'id': 1,
                                               'destination': '+15145550000',
                                               'destination_type': 'office_phone' },
                                             { 'destination': '+15145550001',
                                               'destination_type': 'cell_phone' }]}
                                    })
        expected_error = json.dumps({'error':'Some entered values are incorrect.', 'attributes':{'email':['cannot be blank']}})
        self.client._do_patch = Mock(side_effect=SendSecureException(400, expected_error, ''))
        with self.assertRaises(SendSecureException) as context:
            result = self.client.update_favorite(456, favorite_json)
        self.client._do_patch.assert_called_once_with('https://awesome.sendsecure.portal/api/v2/enterprises/acme/users/123456/favorites/456.json',
                                                    'application/json',
                                                    favorite_json,
                                                    'application/json')
        self.assertEqual(context.exception.code, 400)
        self.assertIn(expected_error, context.exception.message)

    def test_delete_favorite_success(self):
        self.client._do_delete = Mock(expected_response=None)
        result = self.client.delete_favorite(456)
        self.client._do_delete.assert_called_once_with('https://awesome.sendsecure.portal/api/v2/enterprises/acme/users/123456/favorites/456.json',
                                                       'application/json')

    def test_delete_favorite_error(self):
        self.client._do_delete = Mock(side_effect=SendSecureException(403, 'Access denied', ''))
        with self.assertRaises(SendSecureException) as context:
            result = self.client.delete_favorite(456)
        self.client._do_delete.assert_called_once_with('https://awesome.sendsecure.portal/api/v2/enterprises/acme/users/123456/favorites/456.json',
                                                       'application/json')
        self.assertEqual(context.exception.code, 403)
        self.assertIn('Access denied', context.exception.message)

    def test_create_participant_success(self):
        participant_json = json.dumps({ 'participant': {
                                            'first_name': 'John',
                                            'last_name': 'Smith',
                                            'company_name': 'ACME',
                                            'email': 'johny.smith@example.com',
                                            'contact_methods': [
                                                { 'destination': '+15145550000',
                                                  'destination_type': 'office_phone' }] }
                                      })
        expected_response = json.dumps({ 'id': '23a3c8ec897548dc82f50a9a1550e52c',
                                         'first_name': 'John',
                                         'last_name': 'Smith',
                                         'email': 'johny.smith@example.com',
                                         'type': 'guest',
                                         'role': 'guest',
                                         'guest_options': {
                                             'company_name': 'ACME',
                                             'locked': False,
                                             'bounced_email': False,
                                             'failed_login_attempts': 0,
                                             'verified': False,
                                             'created_at': '2017-05-26T19:27:27.798Z',
                                             'updated_at': '2017-05-26T19:27:27.798Z',
                                             'contact_methods': [
                                                 { 'id': 35105,
                                                    'destination': '+15145550000',
                                                    'destination_type': 'office_phone',
                                                    'verified': False,
                                                    'created_at': '2017-05-26T19:27:27.864Z',
                                                    'updated_at': '2017-05-26T19:27:27.864Z' } ] }
                                       })
        self.client._do_post = Mock(return_value=expected_response)
        result = json.loads(self.client.create_participant(self.safebox_guid, participant_json))
        self.client._do_post.assert_called_once_with('https://awesome.sendsecure.portal/api/v2/safeboxes/7a3c51e00a004917a8f5db807180fcc5/participants.json',
                                                       'application/json',
                                                       participant_json,
                                                       'application/json')
        self.assertEqual(result['id'], '23a3c8ec897548dc82f50a9a1550e52c')
        self.assertEqual(result['guest_options']['created_at'], '2017-05-26T19:27:27.798Z')
        self.assertEqual(result['guest_options']['updated_at'], '2017-05-26T19:27:27.798Z')
        self.assertEqual(len(result['guest_options']['contact_methods']), 1)

    def test_create_participant_error(self):
        participant_json = json.dumps({ 'participant': {
                                            'first_name': 'John',
                                            'last_name': 'Smith',
                                            'company_name': 'ACME',
                                            'email': '',
                                            'contact_methods': [
                                                { 'destination': '+15145550000',
                                                  'destination_type': 'office_phone' }] }
                                      })
        expected_error = json.dumps({'error':'Some entered values are incorrect.', 'attributes':{'email':['cannot be blank']}})
        self.client._do_post = Mock(side_effect=SendSecureException(400, expected_error, ''))
        with self.assertRaises(SendSecureException) as context:
            result = self.client.create_participant(self.safebox_guid, participant_json)
        self.client._do_post.assert_called_once_with('https://awesome.sendsecure.portal/api/v2/safeboxes/7a3c51e00a004917a8f5db807180fcc5/participants.json',
                                                    'application/json',
                                                    participant_json,
                                                    'application/json')
        self.assertEqual(context.exception.code, 400)
        self.assertIn(expected_error, context.exception.message)

    def test_update_participant_success(self):
        participant_json = json.dumps({ 'participant': {
                                            'first_name': 'John',
                                            'last_name': 'Smith',
                                            'company_name': 'XMedius',
                                            'email': 'johny.smith@example.com',
                                            'contact_methods': [
                                                { 'id': 32,
                                                  'destination': '+15145550000',
                                                  'destination_type': 'office_phone' }] }
                                      })
        expected_response = json.dumps({ 'id': '23a3c8ec897548dc82f50a9a1550e52c',
                                         'first_name': 'John',
                                         'last_name': 'Smith',
                                         'email': 'johny.smith@example.com',
                                         'type': 'guest',
                                         'role': 'guest',
                                         'guest_options': {
                                             'company_name': 'XMedius',
                                             'locked': False,
                                             'bounced_email': False,
                                             'failed_login_attempts': 0,
                                             'verified': False,
                                             'created_at': '2017-05-26T19:27:27.798Z',
                                             'updated_at': '2017-05-26T19:27:27.798Z',
                                             'contact_methods': [
                                                 {  'id': 32,
                                                    'destination': '+15145550000',
                                                    'destination_type': 'office_phone',
                                                    'verified': False,
                                                    'created_at': '2017-05-26T19:27:27.864Z',
                                                    'updated_at': '2017-05-26T19:27:27.864Z' } ] }
                                       })
        self.client._do_patch = Mock(return_value=expected_response)
        result = json.loads(self.client.update_participant(self.safebox_guid, '23a3c8ec897548dc82f50a9a1550e52c', participant_json))
        self.client._do_patch.assert_called_once_with('https://awesome.sendsecure.portal/api/v2/safeboxes/7a3c51e00a004917a8f5db807180fcc5/participants/23a3c8ec897548dc82f50a9a1550e52c.json',
                                                       'application/json',
                                                       participant_json,
                                                       'application/json')
        self.assertEqual(result['id'], '23a3c8ec897548dc82f50a9a1550e52c')
        self.assertEqual(result['guest_options']['created_at'], '2017-05-26T19:27:27.798Z')
        self.assertEqual(result['guest_options']['updated_at'], '2017-05-26T19:27:27.798Z')
        self.assertEqual(len(result['guest_options']['contact_methods']), 1)

    def test_update_participant_error(self):
        participant_json = json.dumps({ 'participant': {
                                            'first_name': 'John',
                                            'last_name': 'Smith',
                                            'company_name': 'XMedius',
                                            'email': '',
                                            'contact_methods': [
                                                { 'id': 32,
                                                  'destination': '+15145550000',
                                                  'destination_type': 'office_phone' }] }
                                      })
        expected_error = json.dumps({'error':'Some entered values are incorrect.', 'attributes':{'email':['cannot be blank']}})
        self.client._do_patch = Mock(side_effect=SendSecureException(400, expected_error, ''))
        with self.assertRaises(SendSecureException) as context:
            result = self.client.update_participant(self.safebox_guid, '23a3c8ec897548dc82f50a9a1550e52c', participant_json)
        self.client._do_patch.assert_called_once_with('https://awesome.sendsecure.portal/api/v2/safeboxes/7a3c51e00a004917a8f5db807180fcc5/participants/23a3c8ec897548dc82f50a9a1550e52c.json',
                                                       'application/json',
                                                       participant_json,
                                                       'application/json')
        self.assertEqual(context.exception.code, 400)
        self.assertIn(expected_error, context.exception.message)

    def test_search_recipient_success(self):
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
        self.client._do_get = Mock(return_value=expected_response)
        result = json.loads(self.client.search_recipient('john'))
        self.client._do_get.assert_called_once_with('https://awesome.sendsecure.portal/api/v2/recipients/autocomplete?term=john',
                                                       'application/json')
        self.assertEqual(len(result['results']), 3)

    def test_reply_success(self):
        reply_json = json.dumps({ 'safebox': {
                                      'message': 'Test reply message',
                                      'consent': True,
                                      'document_ids': ['1234fdr5ewet5tew4wt'] } })
        expected_response = json.dumps({ 'result': True,
                                         'message': 'SafeBox successfully updated.' })
        self.client._do_post = Mock(return_value=expected_response)
        result = json.loads(self.client.reply(self.safebox_guid, reply_json))
        self.client._do_post.assert_called_once_with('https://awesome.sendsecure.portal/api/v2/safeboxes/7a3c51e00a004917a8f5db807180fcc5/messages.json',
                                                    'application/json',
                                                    reply_json,
                                                    'application/json')
        self.assertTrue(result['result'])
        self.assertEqual(result['message'], 'SafeBox successfully updated.')

    def test_add_time_success(self):
        add_time_json = json.dumps({ 'safebox': { 'add_time_value': 8, 'add_time_unit': 'hours' }})
        expected_response = json.dumps({ 'result': True,
                                         'message': 'SafeBox duration successfully extended.',
                                         'expiration': '2017-05-14T18:09:05.662Z' })
        self.client._do_patch = Mock(return_value=expected_response)
        result = json.loads(self.client.add_time(self.safebox_guid, add_time_json))
        self.client._do_patch.assert_called_once_with('https://awesome.sendsecure.portal/api/v2/safeboxes/7a3c51e00a004917a8f5db807180fcc5/add_time.json',
                                                    'application/json',
                                                    add_time_json,
                                                    'application/json')
        self.assertTrue(result['result'])
        self.assertEqual(result['message'], 'SafeBox duration successfully extended.')
        self.assertEqual(result['expiration'], '2017-05-14T18:09:05.662Z')

    def test_add_time_error(self):
        add_time_json = json.dumps({ 'safebox': { 'add_time_value': 8, 'add_time_unit': 'hours' }})
        expected_error = json.dumps({ 'result': False, 'message': 'Unable to extend the SafeBox duration.' })
        self.client._do_patch = Mock(side_effect=SendSecureException(400, expected_error, ''))
        with self.assertRaises(SendSecureException) as context:
            result = self.client.add_time(self.safebox_guid, add_time_json)
        self.client._do_patch.assert_called_once_with('https://awesome.sendsecure.portal/api/v2/safeboxes/7a3c51e00a004917a8f5db807180fcc5/add_time.json',
                                                    'application/json',
                                                    add_time_json,
                                                    'application/json')
        self.assertEqual(context.exception.code, 400)
        self.assertIn(expected_error, context.exception.message)

    def test_close_safebox_success(self):
        expected_response = json.dumps({ 'result': True, 'message': 'SafeBox successfully closed.' })
        self.client._do_patch = Mock(return_value=expected_response)
        result = json.loads(self.client.close_safebox(self.safebox_guid))
        self.client._do_patch.assert_called_once_with('https://awesome.sendsecure.portal/api/v2/safeboxes/7a3c51e00a004917a8f5db807180fcc5/close.json',
                                                    'application/json',
                                                    '',
                                                    'application/json')
        self.assertTrue(result['result'])
        self.assertEqual(result['message'], 'SafeBox successfully closed.')

    def test_close_safebox_error(self):
        expected_error = json.dumps({ 'result': False, 'message': 'Unable to close the SafeBox.' })
        self.client._do_patch = Mock(side_effect=SendSecureException(400, expected_error, ''))
        with self.assertRaises(SendSecureException) as context:
            result = self.client.close_safebox(self.safebox_guid)
        self.client._do_patch.assert_called_once_with('https://awesome.sendsecure.portal/api/v2/safeboxes/7a3c51e00a004917a8f5db807180fcc5/close.json',
                                                    'application/json',
                                                    '',
                                                    'application/json')
        self.assertEqual(context.exception.code, 400)
        self.assertIn(expected_error, context.exception.message)

    def test_delete_safebox_content_success(self):
        expected_response = json.dumps({ 'result': True, 'message': 'SafeBox content successfully deleted.' })
        self.client._do_patch = Mock(return_value=expected_response)
        result = json.loads(self.client.delete_safebox_content(self.safebox_guid))
        self.client._do_patch.assert_called_once_with('https://awesome.sendsecure.portal/api/v2/safeboxes/7a3c51e00a004917a8f5db807180fcc5/delete_content.json',
                                                    'application/json',
                                                    '',
                                                    'application/json')
        self.assertTrue(result['result'])
        self.assertEqual(result['message'], 'SafeBox content successfully deleted.')

    def test_delete_safebox_content_error(self):
        expected_error = json.dumps({ 'result': False, 'message': 'Unable to delete the SafeBox content.' })
        self.client._do_patch = Mock(side_effect=SendSecureException(400, expected_error, ''))
        with self.assertRaises(SendSecureException) as context:
            result = self.client.delete_safebox_content(self.safebox_guid)
        self.client._do_patch.assert_called_once_with('https://awesome.sendsecure.portal/api/v2/safeboxes/7a3c51e00a004917a8f5db807180fcc5/delete_content.json',
                                                    'application/json',
                                                    '',
                                                    'application/json')
        self.assertEqual(context.exception.code, 400)
        self.assertIn(expected_error, context.exception.message)

    def test_mark_as_read_success(self):
        expected_response = json.dumps({ 'result': True })
        self.client._do_patch = Mock(return_value=expected_response)
        result = json.loads(self.client.mark_as_read(self.safebox_guid))
        self.client._do_patch.assert_called_once_with('https://awesome.sendsecure.portal/api/v2/safeboxes/7a3c51e00a004917a8f5db807180fcc5/mark_as_read.json',
                                                    'application/json',
                                                    '',
                                                    'application/json')
        self.assertTrue(result['result'])

    def test_mark_as_read_error(self):
        expected_error = json.dumps({ 'result': False, 'message': 'Unable to mark the SafeBox as Read.' })
        self.client._do_patch = Mock(side_effect=SendSecureException(400, expected_error, ''))
        with self.assertRaises(SendSecureException) as context:
            result = self.client.mark_as_read(self.safebox_guid)
        self.client._do_patch.assert_called_once_with('https://awesome.sendsecure.portal/api/v2/safeboxes/7a3c51e00a004917a8f5db807180fcc5/mark_as_read.json',
                                                    'application/json',
                                                    '',
                                                    'application/json')
        self.assertEqual(context.exception.code, 400)
        self.assertIn(expected_error, context.exception.message)

    def test_mark_as_unread_success(self):
        expected_response = json.dumps({ 'result': True })
        self.client._do_patch = Mock(return_value=expected_response)
        result = json.loads(self.client.mark_as_unread(self.safebox_guid))
        self.client._do_patch.assert_called_once_with('https://awesome.sendsecure.portal/api/v2/safeboxes/7a3c51e00a004917a8f5db807180fcc5/mark_as_unread.json',
                                                    'application/json',
                                                    '',
                                                    'application/json')
        self.assertTrue(result['result'])

    def test_mark_as_unread_error(self):
        expected_error = json.dumps({ 'result': False, 'message': 'Unable to mark the SafeBox as Unread.' })
        self.client._do_patch = Mock(side_effect=SendSecureException(400, expected_error, ''))
        with self.assertRaises(SendSecureException) as context:
            result = self.client.mark_as_unread(self.safebox_guid)
        self.client._do_patch.assert_called_once_with('https://awesome.sendsecure.portal/api/v2/safeboxes/7a3c51e00a004917a8f5db807180fcc5/mark_as_unread.json',
                                                    'application/json',
                                                    '',
                                                    'application/json')
        self.assertEqual(context.exception.code, 400)
        self.assertIn(expected_error, context.exception.message)


    def test_mark_as_read_message_success(self):
        expected_response = json.dumps({ 'result': True })
        self.client._do_patch = Mock(return_value=expected_response)
        result = json.loads(self.client.mark_as_read_message(self.safebox_guid, 1234))
        self.client._do_patch.assert_called_once_with('https://awesome.sendsecure.portal/api/v2/safeboxes/7a3c51e00a004917a8f5db807180fcc5/messages/1234/read',
                                                    'application/json',
                                                    '',
                                                    'application/json')
        self.assertTrue(result['result'])

    def test_mark_as_read_message_error(self):
        expected_error = json.dumps({ 'result': False, 'message': 'Unable to mark the message as read.' })
        self.client._do_patch = Mock(side_effect=SendSecureException(400, expected_error, ''))
        with self.assertRaises(SendSecureException) as context:
            result = self.client.mark_as_read_message(self.safebox_guid, 1234)
        self.client._do_patch.assert_called_once_with('https://awesome.sendsecure.portal/api/v2/safeboxes/7a3c51e00a004917a8f5db807180fcc5/messages/1234/read',
                                                    'application/json',
                                                    '',
                                                    'application/json')
        self.assertEqual(context.exception.code, 400)
        self.assertIn(expected_error, context.exception.message)

    def test_mark_as_unread_message_success(self):
        expected_response = json.dumps({ 'result': True })
        self.client._do_patch = Mock(return_value=expected_response)
        result = json.loads(self.client.mark_as_unread_message(self.safebox_guid, 1234))
        self.client._do_patch.assert_called_once_with('https://awesome.sendsecure.portal/api/v2/safeboxes/7a3c51e00a004917a8f5db807180fcc5/messages/1234/unread',
                                                    'application/json',
                                                    '',
                                                    'application/json')
        self.assertTrue(result['result'])

    def test_mark_as_unread_message_error(self):
        expected_error = json.dumps({ 'result': False, 'message': 'Unable to mark the message as Unread.' })
        self.client._do_patch = Mock(side_effect=SendSecureException(400, expected_error, ''))
        with self.assertRaises(SendSecureException) as context:
            result = self.client.mark_as_unread_message(self.safebox_guid, 1234)
        self.client._do_patch.assert_called_once_with('https://awesome.sendsecure.portal/api/v2/safeboxes/7a3c51e00a004917a8f5db807180fcc5/messages/1234/unread',
                                                    'application/json',
                                                    '',
                                                    'application/json')
        self.assertEqual(context.exception.code, 400)
        self.assertIn(expected_error, context.exception.message)

    def test_get_file_url_success(self):
        expected_response = json.dumps({ 'url': 'https://fileserver.integration.xmedius.com/xmss/DteeDmb-2zfN5WtCbgpJfSENaNjvbHi_nt' })
        self.client._do_get = Mock(return_value=expected_response)
        result = json.loads(self.client.get_file_url(self.safebox_guid, '154awe5qw4erq5', 'user@email.com'))
        self.client._do_get.assert_called_once_with('https://awesome.sendsecure.portal/api/v2/safeboxes/7a3c51e00a004917a8f5db807180fcc5/documents/154awe5qw4erq5/url.json?user_email=user@email.com',
                                                    'application/json')
        self.assertEqual(result['url'], 'https://fileserver.integration.xmedius.com/xmss/DteeDmb-2zfN5WtCbgpJfSENaNjvbHi_nt')

    def test_get_file_url_error(self):
        expected_error = json.dumps({'error': 'User email not found'})
        self.client._do_get = Mock(side_effect=SendSecureException(400, expected_error, ''))
        with self.assertRaises(SendSecureException) as context:
            result = self.client.get_file_url(self.safebox_guid, '154awe5qw4erq5', 'user@email.com')
        self.client._do_get.assert_called_once_with('https://awesome.sendsecure.portal/api/v2/safeboxes/7a3c51e00a004917a8f5db807180fcc5/documents/154awe5qw4erq5/url.json?user_email=user@email.com',
                                                    'application/json')
        self.assertEqual(context.exception.code, 400)
        self.assertIn(expected_error, context.exception.message)


    def test_get_audit_record_url_success(self):
        expected_response = json.dumps({ 'url': 'http://sendsecure.integration.xmedius.com/s/73af62f766ee459e81f46e4f533085a4.pdf' })
        self.client._do_get = Mock(return_value=expected_response)
        result = json.loads(self.client.get_audit_record_url(self.safebox_guid))
        self.client._do_get.assert_called_once_with('https://awesome.sendsecure.portal/api/v2/safeboxes/7a3c51e00a004917a8f5db807180fcc5/audit_record_pdf.json',
                                                    'application/json')
        self.assertEqual(result['url'], 'http://sendsecure.integration.xmedius.com/s/73af62f766ee459e81f46e4f533085a4.pdf')

    def test_get_audit_record_url_error(self):
        self.client._do_get = Mock(side_effect=SendSecureException(400, 'Access denied', ''))
        with self.assertRaises(SendSecureException) as context:
            result = self.client.get_audit_record_url(self.safebox_guid)
        self.client._do_get.assert_called_once_with('https://awesome.sendsecure.portal/api/v2/safeboxes/7a3c51e00a004917a8f5db807180fcc5/audit_record_pdf.json',
                                                    'application/json')
        self.assertEqual(context.exception.code, 400)
        self.assertIn('Access denied', context.exception.message)

    def test_get_safeboxes_success(self):
        expected_response = json.dumps({ 'count': 1,
                                         'previous_page_url': None,
                                         'next_page_url': 'api/v2/safeboxes?status=unread&search=test&page=2',
                                         'safeboxes': [
                                             {
                                                 'guid': '73af62f766ee459e81f46e4f533085a4',
                                                 'user_id': 1,
                                                 'enterprise_id': 1
                                             }]
                                       })
        self.client._do_get = Mock(return_value=expected_response)
        result = json.loads(self.client.get_safeboxes(None, None))
        self.client._do_get.assert_called_once_with('https://awesome.sendsecure.portal/api/v2/safeboxes.json',
                                                    'application/json')
        self.assertEqual(result['count'], 1)
        self.assertEqual(len(result['safeboxes']), 1)
        self.assertEqual(result['safeboxes'][0]['guid'], '73af62f766ee459e81f46e4f533085a4')

    def test_get_safeboxes_with_search_params_success(self):
        expected_response = json.dumps({ 'count': 1,
                                         'previous_page_url': None,
                                         'next_page_url': 'api/v2/safeboxes?status=unread&search=test&page=2',
                                         'safeboxes': [
                                             {
                                                 'guid': '73af62f766ee459e81f46e4f533085a4',
                                                 'user_id': 1,
                                                 'enterprise_id': 1
                                             }]
                                       })
        self.client._do_get = Mock(return_value=expected_response)
        result = json.loads(self.client.get_safeboxes(None, {'status': 'unread', 'search_term': 'test', 'page': 1}))
        self.client._do_get.assert_called_once_with('https://awesome.sendsecure.portal/api/v2/safeboxes.json?status=unread&search_term=test&page=1',
                                                    'application/json')
        self.assertEqual(result['count'], 1)
        self.assertEqual(len(result['safeboxes']), 1)
        self.assertEqual(result['safeboxes'][0]['guid'], '73af62f766ee459e81f46e4f533085a4')

    def test_get_safeboxes_with_url_success(self):
        expected_response = json.dumps({ 'count': 1,
                                         'previous_page_url': None,
                                         'next_page_url': 'api/v2/safeboxes?status=unread&search=test&page=2',
                                         'safeboxes': [
                                             {
                                                 'guid': '73af62f766ee459e81f46e4f533085a4',
                                                 'user_id': 1,
                                                 'enterprise_id': 1
                                             }]
                                       })
        self.client._do_get = Mock(return_value=expected_response)
        result = json.loads(self.client.get_safeboxes('https://awesome.sendsecure.portal/api/v2/safeboxes.json?status=unread&search_term=test&page=1', None))
        self.client._do_get.assert_called_once_with('https://awesome.sendsecure.portal/api/v2/safeboxes.json?status=unread&search_term=test&page=1',
                                                    'application/json')
        self.assertEqual(result['count'], 1)
        self.assertEqual(len(result['safeboxes']), 1)
        self.assertEqual(result['safeboxes'][0]['guid'], '73af62f766ee459e81f46e4f533085a4')

    def test_get_safeboxes_error(self):
        expected_error = json.dumps({ 'error': 'Invalid per_page parameter value (1001)' })
        self.client._do_get = Mock(side_effect=SendSecureException(400, expected_error, ''))
        with self.assertRaises(SendSecureException) as context:
            result = self.client.get_safeboxes(None, { 'status': 'unread', 'search_term': 'test', 'per_page': 1001, 'page': 2 })
        self.client._do_get.assert_called_once_with('https://awesome.sendsecure.portal/api/v2/safeboxes.json?status=unread&search_term=test&per_page=1001&page=2',
                                                    'application/json')
        self.assertEqual(context.exception.code, 400)
        self.assertIn(expected_error, context.exception.message)

    def test_get_safebox_info_success(self):
        expected_response = json.dumps({ 'safebox': {
                                             'guid': '73af62f766ee459e81f46e4f533085a4',
                                             'security_options': {},
                                             'participants': [],
                                             'messages': [],
                                             'download_activity': {},
                                             'event_history': []
                                         }
                                       })
        self.client._do_get = Mock(return_value=expected_response)
        result = json.loads(self.client.get_safebox_info(self.safebox_guid, None))
        self.client._do_get.assert_called_once_with('https://awesome.sendsecure.portal/api/v2/safeboxes/7a3c51e00a004917a8f5db807180fcc5.json',
                                                    'application/json')
        self.assertEqual(result['safebox']['guid'], '73af62f766ee459e81f46e4f533085a4')
        self.assertFalse(result['safebox']['security_options'])
        self.assertFalse(result['safebox']['participants'])
        self.assertFalse(result['safebox']['messages'])
        self.assertFalse(result['safebox']['download_activity'])
        self.assertFalse(result['safebox']['event_history'])

    def test_get_safebox_info_error(self):
        self.client._do_get = Mock(side_effect=SendSecureException(403, 'Access denied', ''))
        with self.assertRaises(SendSecureException) as context:
            result = self.client.get_safebox_info(self.safebox_guid, None)
        self.client._do_get.assert_called_once_with('https://awesome.sendsecure.portal/api/v2/safeboxes/7a3c51e00a004917a8f5db807180fcc5.json',
                                                    'application/json')
        self.assertEqual(context.exception.code, 403)
        self.assertIn('Access denied', context.exception.message)

    def test_get_safebox_participants_success(self):
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
        self.client._do_get = Mock(return_value=expected_response)
        result = json.loads(self.client.get_safebox_participants(self.safebox_guid))
        self.client._do_get.assert_called_once_with('https://awesome.sendsecure.portal/api/v2/safeboxes/7a3c51e00a004917a8f5db807180fcc5/participants.json',
                                                    'application/json')
        self.assertEqual(len(result['participants']), 2)

    def test_get_safebox_participants_error(self):
        self.client._do_get = Mock(side_effect=SendSecureException(403, 'Access denied', ''))
        with self.assertRaises(SendSecureException) as context:
            result = self.client.get_safebox_participants(self.safebox_guid)
        self.client._do_get.assert_called_once_with('https://awesome.sendsecure.portal/api/v2/safeboxes/7a3c51e00a004917a8f5db807180fcc5/participants.json',
                                                    'application/json')
        self.assertEqual(context.exception.code, 403)
        self.assertIn('Access denied', context.exception.message)

    def test_get_safebox_messages_success(self):
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
        self.client._do_get = Mock(return_value=expected_response)
        result = json.loads(self.client.get_safebox_messages(self.safebox_guid))
        self.client._do_get.assert_called_once_with('https://awesome.sendsecure.portal/api/v2/safeboxes/7a3c51e00a004917a8f5db807180fcc5/messages.json',
                                                    'application/json')
        self.assertEqual(len(result['messages']), 1)
        self.assertEqual(len(result['messages'][0]['documents']), 1)
        self.assertEqual(result['messages'][0]['documents'][0]['id'], '5a3df276aaa24e43af5aca9b2204a535')

    def test_get_safebox_messages_error(self):
        self.client._do_get = Mock(side_effect=SendSecureException(403, 'Access denied', ''))
        with self.assertRaises(SendSecureException) as context:
            result = self.client.get_safebox_messages(self.safebox_guid)
        self.client._do_get.assert_called_once_with('https://awesome.sendsecure.portal/api/v2/safeboxes/7a3c51e00a004917a8f5db807180fcc5/messages.json',
                                                    'application/json')
        self.assertEqual(context.exception.code, 403)
        self.assertIn('Access denied', context.exception.message)

    def test_get_safebox_security_options_success(self):
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
        self.client._do_get = Mock(return_value=expected_response)
        result = json.loads(self.client.get_safebox_security_options(self.safebox_guid))
        self.client._do_get.assert_called_once_with('https://awesome.sendsecure.portal/api/v2/safeboxes/7a3c51e00a004917a8f5db807180fcc5/security_options.json',
                                                    'application/json')
        self.assertTrue(result['security_options'])

    def test_get_safebox_security_options_error(self):
        self.client._do_get = Mock(side_effect=SendSecureException(403, 'Access denied', ''))
        with self.assertRaises(SendSecureException) as context:
            result = self.client.get_safebox_security_options(self.safebox_guid)
        self.client._do_get.assert_called_once_with('https://awesome.sendsecure.portal/api/v2/safeboxes/7a3c51e00a004917a8f5db807180fcc5/security_options.json',
                                                    'application/json')
        self.assertEqual(context.exception.code, 403)
        self.assertIn('Access denied', context.exception.message)

    def test_get_safebox_download_activity_success(self):
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
        self.client._do_get = Mock(return_value=expected_response)
        result = json.loads(self.client.get_safebox_download_activity(self.safebox_guid))
        self.client._do_get.assert_called_once_with('https://awesome.sendsecure.portal/api/v2/safeboxes/7a3c51e00a004917a8f5db807180fcc5/download_activity.json',
                                                    'application/json')
        self.assertEqual(result['download_activity']['guests'][0]['id'], '42220c777c30486e80cd3bbfa7f8e82f')
        self.assertEqual(result['download_activity']['owner']['id'], 72)

    def test_get_safebox_download_activity_error(self):
        self.client._do_get = Mock(side_effect=SendSecureException(403, 'Access denied', ''))
        with self.assertRaises(SendSecureException) as context:
            result = self.client.get_safebox_download_activity(self.safebox_guid)
        self.client._do_get.assert_called_once_with('https://awesome.sendsecure.portal/api/v2/safeboxes/7a3c51e00a004917a8f5db807180fcc5/download_activity.json',
                                                    'application/json')
        self.assertEqual(context.exception.code, 403)
        self.assertIn('Access denied', context.exception.message)

    def test_get_safebox_event_history_success(self):
        expected_response = json.dumps({ 'event_history': [
                                             { 'type': '42220c777c30486e80cd3bbfa7f8e82f',
                                               'date': [],
                                               'metadata': {},
                                               'message': 'SafeBox created by john.smith@example.com with 0 attachment(s) from 0.0.0.0 for john.smith@example.com' }
                                         ]
                                       })
        self.client._do_get = Mock(return_value=expected_response)
        result = json.loads(self.client.get_safebox_event_history(self.safebox_guid))
        self.client._do_get.assert_called_once_with('https://awesome.sendsecure.portal/api/v2/safeboxes/7a3c51e00a004917a8f5db807180fcc5/event_history.json',
                                                    'application/json')
        self.assertEqual(result['event_history'][0]['message'], 'SafeBox created by john.smith@example.com with 0 attachment(s) from 0.0.0.0 for john.smith@example.com')

    def test_get_safebox_event_history_error(self):
        self.client._do_get = Mock(side_effect=SendSecureException(403, 'Access denied', ''))
        with self.assertRaises(SendSecureException) as context:
            result = self.client.get_safebox_event_history(self.safebox_guid)
        self.client._do_get.assert_called_once_with('https://awesome.sendsecure.portal/api/v2/safeboxes/7a3c51e00a004917a8f5db807180fcc5/event_history.json',
                                                    'application/json')
        self.assertEqual(context.exception.code, 403)
        self.assertIn('Access denied', context.exception.message)

    def test_archive_safebox_success(self):
        user_email_json = json.dumps({ 'user_email': 'user@example.com' })
        expected_response = json.dumps({'result': True, 'message': 'SafeBox successfully archived'})
        self.client._do_post = Mock(return_value=expected_response)
        result = json.loads(self.client.archive_safebox(self.safebox_guid, user_email_json))
        self.client._do_post.assert_called_once_with('https://awesome.sendsecure.portal/api/v2/safeboxes/7a3c51e00a004917a8f5db807180fcc5/tag/archive',
                                                    'application/json',
                                                    user_email_json,
                                                    'application/json')
        self.assertTrue(result['result'])
        self.assertEqual(result['message'], 'SafeBox successfully archived')

    def test_archive_safebox_error(self):
        user_email_json = json.dumps({ 'user_email': 'user@example.com' })
        expected_error = json.dumps({ 'result': False, 'message': 'Unable to add Safebox to Archives' })
        self.client._do_post = Mock(side_effect=SendSecureException(400, expected_error, ''))
        with self.assertRaises(SendSecureException) as context:
            result = self.client.archive_safebox(self.safebox_guid, user_email_json)
        self.client._do_post.assert_called_once_with('https://awesome.sendsecure.portal/api/v2/safeboxes/7a3c51e00a004917a8f5db807180fcc5/tag/archive',
                                                    'application/json',
                                                    user_email_json,
                                                    'application/json')
        self.assertEqual(context.exception.code, 400)
        self.assertIn(expected_error, context.exception.message)

    def test_unarchive_safebox_success(self):
        user_email_json = json.dumps({ 'user_email': 'user@example.com' })
        expected_response = json.dumps({'result': True, 'message': 'SafeBox successfully removed from Archives'})
        self.client._do_post = Mock(return_value=expected_response)
        result = json.loads(self.client.unarchive_safebox(self.safebox_guid, user_email_json))
        self.client._do_post.assert_called_once_with('https://awesome.sendsecure.portal/api/v2/safeboxes/7a3c51e00a004917a8f5db807180fcc5/untag/archive',
                                                    'application/json',
                                                    user_email_json,
                                                    'application/json')
        self.assertTrue(result['result'])
        self.assertEqual(result['message'], 'SafeBox successfully removed from Archives')

    def test_unarchive_safebox_error(self):
        user_email_json = json.dumps({ 'user_email': 'user@example.com' })
        expected_error = json.dumps({ 'result': False, 'message': 'Unable to remove Safebox from Archives' })
        self.client._do_post = Mock(side_effect=SendSecureException(400, expected_error, ''))
        with self.assertRaises(SendSecureException) as context:
            result = self.client.unarchive_safebox(self.safebox_guid, user_email_json)
        self.client._do_post.assert_called_once_with('https://awesome.sendsecure.portal/api/v2/safeboxes/7a3c51e00a004917a8f5db807180fcc5/untag/archive',
                                                    'application/json',
                                                    user_email_json,
                                                    'application/json')
        self.assertEqual(context.exception.code, 400)
        self.assertIn(expected_error, context.exception.message)

    def test_get_consent_group_messages_success(self):
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
        self.client._do_get = Mock(return_value=expected_response)
        result = json.loads(self.client.get_consent_group_messages(1))
        self.client._do_get.assert_called_once_with('https://awesome.sendsecure.portal/api/v2/enterprises/acme/consent_message_groups/1',
                                                    'application/json')
        self.assertEqual(result['consent_message_group']['id'], 1)
        self.assertEqual(result['consent_message_group']['consent_messages'][0]['value'], 'Lorem ipsum')

    def test_get_consent_group_messages_error(self):
        self.client._do_get = Mock(side_effect=SendSecureException(404, 'The requested URL cannot be found.', ''))
        with self.assertRaises(SendSecureException) as context:
            result = self.client.get_consent_group_messages(42)
        self.client._do_get.assert_called_once_with('https://awesome.sendsecure.portal/api/v2/enterprises/acme/consent_message_groups/42',
                                                    'application/json')
        self.assertEqual(context.exception.code, 404)
        self.assertIn('The requested URL cannot be found.', context.exception.message)

    def test_unfollow(self):
        expected_response = json.dumps({'result': True, 'message': 'The SafeBox is now unfollowed.'})
        self.client._do_patch = Mock(return_value=expected_response)
        result = json.loads(self.client.unfollow('A-Safebox-Guid'))
        self.assertTrue(result['result'])
        self.assertEqual(result['message'], 'The SafeBox is now unfollowed.')

    def test_unfollow_invalid_safebox_id(self):
        self.client._do_patch = Mock(side_effect=SendSecureException(404, 'The requested URL cannot be found.', ''))
        with self.assertRaises(SendSecureException) as context:
            result = self.client.unfollow('this-safebox-does-not-exist')
        self.client._do_patch.assert_called_once_with('https://awesome.sendsecure.portal/api/v2/safeboxes/this-safebox-does-not-exist/unfollow',
                                                        'application/json', '', 'application/json')
        self.assertEqual(context.exception.code, 404)
        self.assertIn('The requested URL cannot be found.', context.exception.message)

    def test_follow(self):
        expected_response = json.dumps({'result': True, 'message': 'The SafeBox is now followed.'})
        self.client._do_patch = Mock(return_value=expected_response)
        result = json.loads(self.client.unfollow('A-Safebox-Guid'))
        self.assertTrue(result['result'])
        self.assertEqual(result['message'], 'The SafeBox is now followed.')

    def test_follow_invalid_safebox_id(self):
        self.client._do_patch = Mock(side_effect=SendSecureException(404, 'The requested URL cannot be found.', ''))
        with self.assertRaises(SendSecureException) as context:
            result = self.client.follow('this-safebox-does-not-exist')
        self.client._do_patch.assert_called_once_with('https://awesome.sendsecure.portal/api/v2/safeboxes/this-safebox-does-not-exist/follow',
                                                        'application/json', '', 'application/json')
        self.assertEqual(context.exception.code, 404)
        self.assertIn('The requested URL cannot be found.', context.exception.message)


if __name__ == '__main__':
    unittest.main()

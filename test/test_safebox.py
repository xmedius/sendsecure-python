from sendsecure import *
import unittest

class TestSafebox(unittest.TestCase):
    safebox_params = {  'guid': "b4d898ada15f42f293e31905c514607f",
                        'user_id': 1,
                        'enterprise_id': 1,
                        'subject': "Test Subject",
                        'message': "Test Message",
                        'notification_language': "en",
                        'status': "in_progress",
                        'security_profile_name': "security profile",
                        'unread_count': 0,
                        'double_encryption_status': "disabled",
                        'audit_record_pdf': None,
                        'secure_link': None,
                        'secure_link_title': None,
                        'email_notification_enabled': True,
                        'created_at': "2017-05-24T14:45:35.062Z",
                        'updated_at': "2017-05-24T14:45:35.589Z",
                        'assigned_at': "2017-05-24T14:45:35.040Z",
                        'latest_activity': "2017-05-24T14:45:35.544Z",
                        'expiration': "2017-05-31T14:45:35.038Z",
                        'closed_at': None,
                        'content_deleted_at': None,
                        "user_email": "user@example.com",
                        "public_encryption_key": "RBQISzMk9KwkdBKDVw8sQK0gQe4MOTBGaM7hLdVOmJJ56nCZ8N7h2J0Zhy9rb9ax",
                        "security_options": {
                            "security_code_length": 4,
                            "code_time_limit": 5,
                            "allowed_login_attempts": 3,
                            "allow_remember_me": True,
                            "allow_sms": True,
                            "allow_voice": True,
                            "allow_email": False,
                            "reply_enabled": True,
                            "group_replies": False,
                            "expiration_value": 5,
                            "expiration_unit": "days",
                            "retention_period_type": "do_not_discard",
                            "retention_period_value": None,
                            "retention_period_unit": None,
                            "encrypt_message": True,
                            "double_encryption": True,
                            "two_factor_required": True,
                            "auto_extend_value": 3,
                            "auto_extend_unit": "days",
                            "delete_content_on": None,
                            "allow_manual_delete": True,
                            "allow_manual_close": False,
                        },
                        "participants": [{
                            "id": "7a3c51e00a004917a8f5db807180fcc5",
                            "first_name": "Test",
                            "last_name": "Participant",
                            "email": "participant@example.com",
                            "guest_options": {
                              "company_name": "Test Company",
                              "bounced_email": False,
                              "failed_login_attempts": 0,
                              "verified": False,
                              "contact_methods": [{ "destination": "+15145550000",
                                                    "destination_type": "office_phone",
                                                    "verified": False,
                                                    "created_at": "2017-04-28T17:14:55.304Z",
                                                    "updated_at": "2017-04-28T17:14:55.304Z" }]
                            }
                        },
                        { "id": "1",
                          "first_name": "Jane",
                          "last_name": "Doe",
                          "email": "jane.doe@example.com",
                          "type": "user",
                          "role": "owner"}
                        ],
                        "messages": [{
                            "note": "Lorem Ipsum...",
                            "note_size": 123,
                            "read": True,
                            "author_id": "1",
                            "author_type": "guest",
                            "created_at": "2017-04-05T14:49:35.198Z",
                            "documents": [{
                              "id": "5a3df276aaa24e43af5aca9b2204a535",
                              "name": "Axient-soapui-project.xml",
                              "sha": "724ae04430315c60ca17f4dbee775a37f5b18c91fde6eef24f77a605aee99c9c",
                              "size": 12345,
                              "url": "https://sendsecure.integration.xmedius.com/api/v2/safeboxes/b4d898ada15f42f293e31905c514607f/documents/5a3df276aaa24e43af5aca9b2204a535/url"
                            }]
                        }],
                        "download_activity": {
                            "guests": [{
                              "id": "42220c777c30486e80cd3bbfa7f8e82f",
                              "documents": [{
                                "id": "5a3df276aaa24e43af5aca9b2204a535",
                                "downloaded_bytes": 0,
                                "download_date": None
                              }]
                            }],
                            "owner": {
                              "id": 1,
                              "documents": []
                            }
                        },
                        "event_history": [{
                            "type": "safebox_created_owner",
                            "date": "2017-03-30T18:09:05.966Z",
                            "metadata": {
                              "emails": [
                                "john44@example.com"
                              ],
                              "attachment_count": 0
                            },
                            "message": "message"
                        }]
                    }

    def setUp(self):
        pass

    def test_initialization_with_json_params(self):
        safebox = Safebox(params=json.dumps(self.safebox_params))
        self.assertEqual(safebox.guid, "b4d898ada15f42f293e31905c514607f")
        self.assertIsInstance(safebox.security_options, SecurityOptions)
        self.assertIsInstance(safebox.participants[0], Participant)
        self.assertIsInstance(safebox.participants[0].guest_options, GuestOptions)
        self.assertIsInstance(safebox.download_activity, DownloadActivity)
        self.assertIsInstance(safebox.download_activity.guests[0], DownloadActivityDetail)
        self.assertIsInstance(safebox.download_activity.guests[0].documents[0], Document)
        self.assertIsInstance(safebox.messages[0], Message)
        self.assertIsInstance(safebox.messages[0].documents[0], Document)
        self.assertIsInstance(safebox.event_history[0], EventHistory)

    def test_initialization_without_params(self):
        safebox = Safebox(user_email="user@example.com")
        self.assertEqual(len(safebox.participants), 0)
        self.assertEqual(safebox.user_email, "user@example.com")
        self.assertEqual(safebox.notification_language, "en")
        self.assertEqual(len(safebox.attachments), 0)
        self.assertIsInstance(safebox.security_options, SecurityOptions)

    def test_update_attributes_default(self):
        safebox = Safebox(user_email="user2@example.com")
        safebox.update_attributes(self.safebox_params)
        self.assertEqual(safebox.user_email, "user@example.com")
        self.assertIsInstance(safebox.security_options, SecurityOptions)
        self.assertIsInstance(safebox.participants[0], Participant)
        self.assertIsInstance(safebox.participants[0].guest_options, GuestOptions)
        self.assertIsInstance(safebox.download_activity, DownloadActivity)
        self.assertIsInstance(safebox.download_activity.guests[0], DownloadActivityDetail)
        self.assertIsInstance(safebox.download_activity.guests[0].documents[0], Document)
        self.assertIsInstance(safebox.messages[0], Message)
        self.assertIsInstance(safebox.messages[0].documents[0], Document)
        self.assertIsInstance(safebox.event_history[0], EventHistory)

    def test_update_attributes_on_creation(self):
        safebox = Safebox(user_email="user2@example.com")
        on_creation_params = {  'guid': "b4d898ada15f42f293e31905c514607f",
                                'user_id': 1,
                                'enterprise_id': 1,
                                'subject': "Test Subject",
                                'expiration': "2017-05-31T14:42:27.258Z",
                                'notification_language': "en",
                                'status': "in_progress",
                                'security_profile_name': "security profile",
                                'force_expiry_date': None,
                                "security_code_length": 4,
                                "allowed_login_attempts": 3,
                                "allow_remember_me": True,
                                "allow_sms": True,
                                "allow_voice": True,
                                "allow_email": False,
                                "reply_enabled": True,
                                "group_replies": False,
                                "code_time_limit": 5,
                                "encrypt_message": True,
                                "two_factor_required": True,
                                "auto_extend_value": 3,
                                "auto_extend_unit": "days",
                                "retention_period_type": "do_not_discard",
                                "retention_period_value": None,
                                "retention_period_unit": "hours",
                                "delete_content_on": None,
                                "allow_manual_delete": True,
                                "allow_manual_close": False,
                                'email_notification_enabled': True,
                                'preview_url': "https://sendsecure.integration.xmedius.com/s/845459484b674055bec4ddf2ba5ab60e/preview",
                                'encryption_key': None,
                                'created_at': "2017-05-24T14:42:27.289Z",
                                'updated_at': "2017-05-24T14:42:27.526Z",
                                'latest_activity': "2017-05-24T14:42:27.463Z"
                            }
        on_creation_params['is_creation'] = True
        safebox.update_attributes(on_creation_params)
        self.assertEqual(safebox.guid, "b4d898ada15f42f293e31905c514607f")
        self.assertIsInstance(safebox.security_options, SecurityOptions)
        self.assertEqual(safebox.security_options.encrypt_message, True)

    def test_to_json_all_attributes_configured(self):
        expected_json = {"safebox": {
                            "guid": "b4d898ada15f42f293e31905c514607f",
                            "recipients": [{
                                "first_name": "Test",
                                "last_name": "Participant",
                                "company_name": "Test Company",
                                "email": "participant@example.com",
                                "contact_methods": [{
                                    "destination_type": "office_phone",
                                    "destination": "+15145550000"
                                }]
                            }],
                            "subject": "Test Subject",
                            "message": "Test Message",
                            "document_ids": [],
                            "reply_enabled": True,
                            "group_replies": False,
                            "expiration_value": 5,
                            "expiration_unit": "days",
                            "retention_period_type": "do_not_discard",
                            "encrypt_message": True,
                            "double_encryption": True,
                            "email_notification_enabled": True,
                            "public_encryption_key": "RBQISzMk9KwkdBKDVw8sQK0gQe4MOTBGaM7hLdVOmJJ56nCZ8N7h2J0Zhy9rb9ax",
                            "notification_language": "en",
                            "user_email": "user@example.com"
                        }
                    }
        safebox = Safebox(params=self.safebox_params)
        self.assertEqual(safebox.to_json(), json.dumps(expected_json, sort_keys=True))

if __name__ == '__main__':
    unittest.main()

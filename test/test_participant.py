from sendsecure import *
import unittest

class TestParticipant(unittest.TestCase):
    participant_params = {  'email': "participant@example.com",
                            'id': "7a3c51e00a004917a8f5db807180fcc5",
                            'first_name': "Test",
                            'last_name': "Participant",
                            'type': "guest",
                            'role': "guest",
                            "privileged": True,
                            'guest_options': {
                                'locked': False,
                                'bounced_email': False,
                                'failed_login_attempts': 0,
                                'verified': False,
                                'created_at': "2017-04-12T15:41:39.767Z",
                                'updated_at': "2017-04-12T15:41:47.144Z",
                                'company_name': "Test Company",
                                'contact_methods': [{
                                    'id': 1,
                                    'verified': False,
                                    'destination': "514-555-0001",
                                    'destination_type': "cell_phone",
                                    'created_at': "2017-04-28T17:14:55.304Z",
                                    'updated_at': "2017-04-28T17:14:55.304Z"
                                }]
                            }
                        }

    def setUp(self):
        pass

    def test_initialization_with_json_params(self):
        participant = Participant(params=json.dumps(self.participant_params))
        self.assertEqual(participant.email, "participant@example.com")
        options = participant.guest_options
        self.assertIsInstance(options, GuestOptions)
        self.assertEqual(len(options.contact_methods), 1)
        self.assertIsInstance(options.contact_methods[0], ContactMethod)

    def test_initialization_with_dict_params(self):
        participant = Participant(params=self.participant_params)
        self.assertEqual(participant.email, "participant@example.com")
        options = participant.guest_options
        self.assertIsInstance(options, GuestOptions)
        self.assertEqual(len(options.contact_methods), 1)
        self.assertIsInstance(options.contact_methods[0], ContactMethod)

    def test_initialization_without_params(self):
        participant = Participant(email="participant@example.com")
        self.assertIsNone(participant.first_name)
        self.assertEqual(participant.email, "participant@example.com")
        self.assertIsInstance(participant.guest_options, GuestOptions)
        self.assertEqual(len(participant.guest_options.contact_methods), 0)

    def test_update_attributes(self):
        participant = Participant(email="participant2@example.com")
        participant.update_attributes(self.participant_params)
        self.assertEqual(participant.id, "7a3c51e00a004917a8f5db807180fcc5")
        self.assertEqual(participant.email, "participant@example.com")
        options = participant.guest_options
        self.assertIsInstance(options, GuestOptions)
        self.assertEqual(len(options.contact_methods), 1)
        self.assertIsInstance(options.contact_methods[0], ContactMethod)
        self.assertEqual(options.contact_methods[0].id, 1)

    def test_contact_methods_removed(self):
        participant = Participant(email="participant@example.com")
        participant.guest_options.contact_methods.append(ContactMethod({'id': 2, 'destination': "514-555-0001"}))
        participant.update_attributes(self.participant_params)
        options = participant.guest_options
        self.assertEqual(len(options.contact_methods), 1)
        self.assertIsInstance(options.contact_methods[0], ContactMethod)
        self.assertEqual(options.contact_methods[0].id, 1)

    def test_to_json_all_attributes_configured(self):
        expected_json = {"participant": {
                            "contact_methods": [{
                                "destination": "514-555-0001",
                                "id": 1,
                                "destination_type": "cell_phone"
                            }],
                            "first_name": "Test",
                            "last_name": "Participant",
                            "locked": False,
                            "company_name": "Test Company",
                            "email": "participant@example.com",
                            "privileged": True
                        }
                    }

        participant = Participant(params=self.participant_params)
        self.assertEqual(participant.to_json(), json.dumps(expected_json, sort_keys=True))

    def test_to_json_some_attributes_configured(self):
        expected_json = {"participant": {
                            "contact_methods": [],
                            "email": "participant@example.com"
                            }
                        }
        participant = Participant(email="participant@example.com")
        self.assertEqual(participant.to_json(), json.dumps(expected_json, sort_keys=True))

    def test_contact_deletable(self):
        expected_json = {"participant": {
                            "contact_methods": [{
                                "destination": "514-555-0001",
                                "id": 1,
                                "_destroy": True,
                                "destination_type": "cell_phone"
                            }],
                            "first_name": "Test",
                            "last_name": "Participant",
                            "locked": False,
                            "company_name": "Test Company",
                            "email": "participant@example.com",
                            "privileged": True
                        }
                    }
        participant = Participant(params=self.participant_params)
        participant.guest_options.contact_methods[0]._destroy = True
        self.assertEqual(participant.to_json(), json.dumps(expected_json, sort_keys=True))

if __name__ == '__main__':
    unittest.main()

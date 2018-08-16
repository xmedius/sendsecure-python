from sendsecure import *
import unittest

class TestFavorite(unittest.TestCase):
    favorite_params = { 'email': "favorite@example.com",
                        'id': 1,
                        'first_name': "Test",
                        'last_name': "Favorite",
                        'company_name': "Test Company",
                        'order_number': 1,
                        'created_at': "2017-04-12T15:41:39.767Z",
                        'updated_at': "2017-04-12T15:41:47.144Z",
                        'contact_methods': [{
                            'id': 1,
                            'destination': "514-555-0001",
                            'destination_type': "cell_phone",
                            'created_at': "2017-04-28T17:14:55.304Z",
                            'updated_at': "2017-04-28T17:14:55.304Z"
                        }]
                    }

    def setUp(self):
        pass

    def test_initialization_with_json_params(self):
        favorite = Favorite(params=json.dumps(self.favorite_params))
        self.assertEqual(len(favorite.contact_methods), 1)
        self.assertIsInstance(favorite.contact_methods[0], ContactMethod)
        self.assertEqual(favorite.email, "favorite@example.com")

    def test_initialization_with_dict_params(self):
        favorite = Favorite(params=self.favorite_params)
        self.assertEqual(len(favorite.contact_methods), 1)
        self.assertIsInstance(favorite.contact_methods[0], ContactMethod)
        self.assertEqual(favorite.email, "favorite@example.com")

    def test_initialization_without_params(self):
        favorite = Favorite(email="favorite@example.com")
        self.assertIsNone(favorite.first_name)
        self.assertEqual(len(favorite.contact_methods), 0)
        self.assertEqual(favorite.email, "favorite@example.com")

    def test_update_attributes(self):
        favorite = Favorite(email="favorite2@example.com")
        favorite.update_attributes(self.favorite_params)
        self.assertEqual(favorite.email, "favorite@example.com")
        self.assertEqual(favorite.id, 1)
        self.assertEqual(len(favorite.contact_methods), 1)
        self.assertIsInstance(favorite.contact_methods[0], ContactMethod)
        self.assertEqual(favorite.contact_methods[0].id, 1)

    def test_contact_methods_removed(self):
        favorite = Favorite(email="favorite@example.com")
        favorite.contact_methods.append(ContactMethod({'id': 2, 'destination': "514-555-0001"}))
        favorite.update_attributes(self.favorite_params)
        self.assertEqual(len(favorite.contact_methods), 1)
        self.assertIsInstance(favorite.contact_methods[0], ContactMethod)
        self.assertEqual(favorite.contact_methods[0].id, 1)

    def test_to_json_all_attributes_configured(self):
        expected_json = {"favorite": {
                            "first_name": "Test",
                            "last_name": "Favorite",
                            "contact_methods": [{
                                "destination": "514-555-0001",
                                "id": 1,
                                "destination_type": "cell_phone"
                            }],
                            "company_name": "Test Company",
                            "order_number": 1,
                            "email": "favorite@example.com"
                        }
                    }

        favorite = Favorite(params=self.favorite_params)
        self.assertEqual(favorite.to_json(), json.dumps(expected_json, sort_keys=True))

    def test_to_json_some_attributes_configured(self):
        expected_json = {"favorite": {
                            "contact_methods": [],
                            "email": "favorite@example.com"
                            }
                        }
        favorite = Favorite(email="favorite@example.com")
        self.assertEqual(favorite.to_json(), json.dumps(expected_json, sort_keys=True))

    def test_contact_deletable(self):
        expected_json = {"favorite": {
                            "first_name": "Test",
                            "last_name": "Favorite",
                            "contact_methods": [{
                                "destination": "514-555-0001",
                                "id": 1,
                                "destination_type": "cell_phone",
                                "_destroy": True
                            }],
                            "company_name": "Test Company",
                            "order_number": 1,
                            "email": "favorite@example.com"
                        }
                    }
        favorite = Favorite(params=self.favorite_params)
        favorite.contact_methods[0]._destroy = True
        self.assertEqual(favorite.to_json(), json.dumps(expected_json, sort_keys=True))

if __name__ == '__main__':
    unittest.main()

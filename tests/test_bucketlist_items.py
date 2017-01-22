from .test_base import TestBase
from werkzeug.exceptions import NotFound, Forbidden
from app.exceptions import ConflictError


class TestBucketlistItems(TestBase):
    """ Test users' Bucketlist items """

    def test_add_bucketlist_item(self):
        """ Test for new item creation """
        res, json = self.client.post('/api/v1/bucketlists/1/items/',
                                     data={'name': 'Prepare for launch'})
        self.assertEqual(res.status_code, 201)
        self.assertTrue(
            json['message'],
            "Bucketlist item successfuly created"
        )
        location = res.headers['Location']
        res1, json1 = self.client.get(location)
        self.assertEqual(res1.status_code, 200)
        self.assertIn('Prepare', json1['name'])
        self.assertEqual(json1['self_url'], location)
        self.assertTrue(not json1['description'])

    def test_update_bucketlist_item(self):
        """ Test for updating an item """
        res, json = self.client.put('/api/v1/bucketlists/1/items/1',
                                    data={"name": "Edited item name"})
        self.assertEqual(res.status_code, 200)
        self.assertTrue(
            json['message'],
            "Bucketlist item successfuly updated"
        )

    def test_delete_bucketlist_item(self):
        """ Test deletion of a bucketlist item """
        res, json = self.client.delete('/api/v1/bucketlists/1/items/1')
        self.assertEqual(res.status_code, 200)
        self.assertTrue(
            json['message'],
            "Your bucketlist item was successfuly deleted"
        )

    def test_get_bucketlist_item(self):
        """ Test that we can fetch a specific bucket list item """
        # Get bucket list whose ID is 1
        res, json = self.client.get('/api/v1/bucketlists/1/items/1')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Ndoo4', json['name'])
        self.assertTrue(json['description'] == '')

    def test_get_bucketlist_items(self):
        """ Test that all bucketlist items are returned """
        res, json = self.client.get('/api/v1/bucketlists/1/items/')
        self.assertEqual(res.status_code, 200)

    def test_operations_on_invalid_bucketlist_item(self):
        """
        Tests to cover all invalid bucketlist items scenarios
        """
        with self.assertRaises(NotFound):
            res1, json1 = self.client.get('/api/v1/bucketlists/1/items/233')
            self.assertEqual(res1.status_code, 404)
            self.assertTrue(
                json1['message'],
                "The requested bucketlist item does not exist"
            )

        """ Test editing a bucketlist item that doesn't exist """
        with self.assertRaises(NotFound):
            res2, json2 = self.client.put('/api/v1/bucketlists/1/items/221',
                                          data={
                                            "name": "ndoo5",
                                            "description": "no desc"
                                          })
            self.assertEqual(res2.status_code, 404)
            self.assertTrue(
                json['message'],
                "Cannot edit a bucketlist item that does not exist"
            )

        """ Test deletion of a bucketlist item that does not exist """
        with self.assertRaises(NotFound):
            res3, json3 = self.client.delete('/api/v1/bucketlists/1/items/221')
            self.assertEqual(res3.status_code, 404)
            self.assertTrue(
                json3['message'],
                "Cannot delete a bucketlist item that does not exist"
            )

    def test_add_duplicate_bucketlist_item(self):
        """ Test creation of a bucketlist item with an existing name """
        with self.assertRaises(ConflictError):
            res, json = self.client.post('/api/v1/bucketlists/1/items/',
                                         data={
                                            "name": "Build a Time Machine"
                                         })
            self.assertEqual(res.status_code, 409)
            self.assertTrue(
                json['message'],
                "You already have a bucketlist item with that name"
            )

    def test_non_existent_bucketlists_and_items(self):
        """
        Tests to cover all invalid bucketlists scenarios
        """
        with self.assertRaises(NotFound):
            res1, json1 = self.client.get('/api/v1/bucketlists/198/items/1')
            self.assertEqual(res1.status_code, 404)
            self.assertTrue(
                json1['message'],
                "The bucketlist does not exist"
            )

        """ Test editing a bucketlist that doesn't exist """
        with self.assertRaises(NotFound):
            res2, json2 = self.client.put('/api/v1/bucketlists/456/items/1',
                                          data={
                                            "name": "ndoo5",
                                            "description": "no desc"
                                          })
            self.assertEqual(res2.status_code, 404)
            self.assertTrue(
                json['message'],
                "Cannot edit a bucketlist that does not exist"
            )

        """ Test deletion of a bucketlist that does not exist """
        with self.assertRaises(NotFound):
            res3, json3 = self.client.delete('/api/v1/bucketlists/61/items/1')
            self.assertEqual(res3.status_code, 404)
            self.assertTrue(
                json3['message'],
                "Cannot delete a bucketlist that does not exist"
            )

    def test_bucketlist_item_operations_on_another_users_bucketlist(self):
        """ Test that users cannot access other users' bucketlist items """
        # Attempt to get another user's bucketlist item
        with self.assertRaises(Forbidden):
            res1, json1 = self.client2.get('/api/v1/bucketlists/1/items/')
            self.assertEqual(res1.status_code, 403)
            self.assertTrue(
                json1['message'],
                "You do not have permission to access this resource"
            )

        # Attempt to update another user's bucketlist item
        with self.assertRaises(Forbidden):
            res2, json2 = self.client2.put('/api/v1/bucketlists/1/items/1',
                                           data={
                                            "name": "ndoo6",
                                            "description": "desc"
                                           })
            self.assertEqual(res2.status_code, 403)
            self.assertTrue(
                json2['message'],
                "You do not have permission to edit this resource"
            )

        """ Test deletion of another user's bucketlist item"""
        with self.assertRaises(Forbidden):
            res3, json3 = self.client2.delete('/api/v1/bucketlists/1/items/1')
            self.assertEqual(res3.status_code, 403)
            self.assertTrue(
                json3['message'],
                "You do not have permission to delete this resource"
            )

        """ Test creation of an item in another user's bucketlist """
        with self.assertRaises(Forbidden):
            res4, json4 = self.client2.post('/api/v1/bucketlists/1/items/',
                                            data={"name": "New Item 123"})
            self.assertEqual(res4.status_code, 403)
            self.assertTrue(
                json4['message'],
                "You do not have permission to add an item to another user's \
                bucketlist"
            )

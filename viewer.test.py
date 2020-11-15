import unittest
import os
import requests

from viewer import app

class ViewerTestCases(unittest.TestCase):
    def test_viewer(self):
        tester = app.test_client(self)
        response = tester.get('/')
        self.assertEqual(response.status_code, 200) # checks that server is live
        self.assertTrue(b'I need help' in response.data) # checks that "I need help" has been loaded onto page
        self.assertEqual(response.data.count(b'class="item'), 102) # checks that there are 102 tickets
        self.assertEqual(response.data.count(b'class="popup'), 102) # checks that there are 102 popup panels
        self.assertEqual(response.data.count(b'class="carousel-item'), 5) # checks that there are 5 pages

    def test_error(self):
        correct_username = app.config['zendesk_username']
        correct_password = app.config['zendesk_password']
        app.config['zendesk_username'] = 'wrong_username' # assigns an incorrect username and password
        app.config['zendesk_password'] = 'wrong_password'
        tester = app.test_client(self)
        response = tester.get('/')
        self.assertTrue(b'Unable to reach Zendesk API' in response.data) # checks that error page has loaded
        app.config['zendesk_username'] = correct_username
        app.config['zendesk_password'] = correct_password

    def test_addJson(self):
        url = 'https://' + app.config['zendesk_subdomain'] + '.zendesk.com/api/v2/tickets.json'
        r = requests.post(url, auth=(app.config['zendesk_username'], app.config['zendesk_password']), json={"ticket": {"subject": "My printer is on fire!", "comment": { "body": "The smoke is very colorful." }}})

        tester = app.test_client(self)
        response = tester.get('/')
        self.assertEqual(response.data.count(b'class="item'), 103) # checks that there are now 103 tickets

        response_json = r.json()
        delete_id = response_json['ticket']['id']
        delete_url = 'https://' + app.config['zendesk_subdomain'] + '.zendesk.com/api/v2/tickets/' + str(delete_id) + '.json'
        requests.delete(delete_url, auth=(app.config['zendesk_username'], app.config['zendesk_password']))

if __name__ == '__main__':
    unittest.main()
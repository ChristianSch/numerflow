import requests


class ApiController(object):
    user_name = None
    auth_token = None

    def __init__(self):
        pass

    def login(self, user_name, user_password):
        r = requests.post('https://api.numer.ai/login',
                          data={'email': user_name,
                                'password': user_password})

        r.raise_for_status()
        r_json = r.json()

        self.user_name = r_json['username']
        self.auth_token = r_json['accessToken']

        return r_json

    def fetch_submissions(self, usern=None):
        if usern:
            requests.get('https://api.numer.ai/user/' % (usern)).json()

        if self.auth_token:
            r = requests.get('https://api.numer.ai/user/%s' % (self.user_name),
                             headers={'Authorization': 'Bearer %s'
                                      % (self.auth_token)})
            r.raise_for_status
            return r.json()

    def upload_submission(self, file_path):
        headers = {}

        if self.auth_token:
            headers = {
                'Authorization': 'Bearer %s' % (self.auth_token)
            }

        req1 = requests.post('https://api.numer.ai/upload/auth')
        r = requests.post('https://api.numer.ai/submissions',
                          data={}, headers=headers)

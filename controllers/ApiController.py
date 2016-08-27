from datetime import datetime
from datetime import timedelta
import os

import requests


class ApiController(object):
    user_name = None
    auth_token = None

    def __init__(self):
        pass

    def login(self, user_mail, user_password):
        r = requests.post('https://api.numer.ai/login',
                          data={'email': user_mail,
                                'password': user_password})

        r.raise_for_status()
        r_json = r.json()

        self.user_name = r_json['username']
        self.auth_token = r_json['accessToken']

        return r_json

    def fetch_submissions(self, usern=None):
        """
        Fetches the submissions for either usern (unauthorized, read,
        without filenames) or the authorized user.

        @param usern Username for the unauthorized submission fetching request.
                     Note: if set, this is prioritized over the authorized
                     user.

        @returns Either the submissions or `None`.
        """
        if usern:
            r = requests.get('https://api.numer.ai/user/' % (usern))
            r.raise_for_status
            return r.json()

        elif self.auth_token:
            r = requests.get('https://api.numer.ai/user/%s' % (self.user_name),
                             headers={'Authorization': 'Bearer %s'
                                      % (self.auth_token)})
            r.raise_for_status
            return r.json()

        else:
            return None

    def fetch_competitions(self):
        """
        Fetches current and if provided, the upcoming competition.
        """
        now = datetime.now()
        d = timedelta(microseconds=55296e5)
        dt = now - d
        dt_str = dt.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

        url = 'https://api.numer.ai/competitions?{ leaderboard :'
        url += ' current , end_date :{ $gt : %s }}'
        r = requests.get((url % (dt_str)).replace(' ', '%22'))
        r.raise_for_status

        return r.json()

    def fetch_current_competition(self):
        """
        Fetches the current competition.
        """
        now = datetime.now()
        comps = self.fetch_competitions()

        for comp in comps:
            start_date = datetime.strptime(comp['start_date'],
                                           '%Y-%m-%dT%H:%M:%S.%fZ')
            end_date = datetime.strptime(comp['end_date'],
                                         '%Y-%m-%dT%H:%M:%S.%fZ')

            if start_date < now < end_date:
                return comp

    def fetch_current_dataset_uri(self):
        """
        Fetches the URI of the dataset for the running round.
        """
        BASE_URL = 'https://datasets.numer.ai/{0}/numerai_datasets.zip'

        try:
            did = self.fetch_current_competition()['dataset_id'][0:7]
        except KeyError, e:
            print 'Competition data might have changed. Received no dataset id'
            raise e

        if did:
            return BASE_URL.format(did)

        return None

    def upload_submission(self, file_path):
        """
        Uploads a submission to S3 and submits it to numer.ai

        @param file_path Path to file for upload. Ought to be a csv.
        """
        file_name = os.path.split(file_path)[1]

        headers = {
            'Authorization': 'Bearer %s' % (self.auth_token)
        }

        # authorize upload
        req1 = requests.post('https://api.numer.ai/upload/auth',
                             data={'filename': file_name,
                                   'mimetype': 'text/csv'},
                             headers=headers)
        req1.raise_for_status
        req1_data = req1.json()

        with open(file_path, 'rb') as fp:
            req = requests.Request('PUT', req1_data['signedRequest'],
                                   data=fp.read())

            r = req.prepare()

            s = requests.Session()
            res = s.send(r)
            res.raise_for_status

            fp.close()

        comp = self.fetch_current_competition()

        r = requests.post('https://api.numer.ai/submissions',
                          data={'competition_id': comp['_id'],
                                'dataset_id': comp['dataset_id'],
                                'filename': req1_data['filename']},
                          headers=headers)

        r.raise_for_status

    def fetch_prediction_count(self):
        """
        Returns the count of all predictions made.

        @returns number of predictions as int
        """
        r = requests.get('https://api.numer.ai/stats').json()
        r.raise_for_status
        return r.json()['predictions']

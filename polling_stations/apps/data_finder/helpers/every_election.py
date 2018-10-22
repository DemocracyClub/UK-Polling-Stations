import requests
from django.conf import settings
from uk_geo_utils.helpers import Postcode


class EveryElectionWrapper:

    def __init__(self, postcode=None, point=None):
        if not postcode and not point:
            raise ValueError('Expected either a point or a postcode')
        try:
            self.request_success = False
            if postcode:
                self.elections = self.get_data_by_postcode(Postcode(postcode).with_space)
                self.request_success = True
            elif point:
                self.elections = self.get_data_by_point(point)
                self.request_success = True
        except Exception:
            self.request_success = False

    def get_data_by_postcode(self, postcode):
        query_url = "%sapi/elections.json?postcode=%s&future=1" % (
            settings.EE_BASE, postcode)
        return self.get_data(query_url)

    def get_data_by_point(self, point):
        query_url = "%sapi/elections.json?coords=%s,%s&future=1" % (
            settings.EE_BASE, point.y, point.x)
        return self.get_data(query_url)

    def get_data(self, query_url):
        headers = {}
        if hasattr(settings, 'CUSTOM_UA'):
            headers['User-Agent'] = settings.CUSTOM_UA

        res = requests.get(query_url, timeout=4, headers=headers)

        if res.status_code != 200:
            res.raise_for_status()

        res_json = res.json()
        return res_json['results']

    def has_election(self):
        if not settings.EVERY_ELECTION['CHECK']:
            return settings.EVERY_ELECTION['HAS_ELECTION']

        if not self.request_success:
            # if the request was unsucessful for some reason,
            # assume there *is* an upcoming election
            return True

        ballots = filter(lambda e: e['group_type'] is None, self.elections)
        ballots = filter(lambda e: e['election_id'] not in settings.ELECTION_BLACKLIST, ballots)

        try:
            next(ballots)
            return True
        except StopIteration:
            return False

    def get_explanations(self):
        explanations = []
        if not self.request_success:
            # if the request was unsucessful for some reason,
            # return no explanations
            return explanations

        if len(self.elections) > 0:
            for election in self.elections:
                if 'explanation' in election and election['explanation']:
                    explanations.append({
                        'title': election['election_title'],
                        'explanation': election['explanation'],
                    })
        return explanations

    def get_metadata(self):
        if not self.request_success:
            return None
        if len(self.elections) > 0:
            for election in self.elections:
                if not 'metadata' in election:
                    continue
                if not election['metadata']:
                    continue
                return election['metadata']
        return None

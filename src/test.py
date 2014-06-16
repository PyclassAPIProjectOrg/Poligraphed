#!flask/bin/python
import os
import unittest
import requests
import json
import pprint
print os.getcwd()
from apikey import _API_KEY
from config import API_KEY
from config import basedir
from app import app, db
from app.models import User
from app.date_convert import javascript_timestamp
from app.cw_api import cw_search_keywords, add_all


class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_make_unique_nickname(self):
        u = User(nickname = 'john', email = 'john@example.com')
        db.session.add(u)
        db.session.commit()
        nickname = User.make_unique_nickname('john')
        assert nickname != 'john'
        u = User(nickname = nickname, email = 'susan@example.com')
        db.session.add(u)
        db.session.commit()
        nickname2 = User.make_unique_nickname('john')
        assert nickname2 != 'john'
        assert nickname2 != nickname

    def test_API_KEY(self):
        API_KEY = _API_KEY
        query_params = { 'apikey': API_KEY,
                         'phrase': 'fiscal cliff' 
                       }
        endpoint = 'http://capitolwords.org/api/text.json'
        response = requests.get( endpoint, params=query_params)
        data = response.json
        pprint.pprint(data)

    def test_apikey(self):
        expected = API_KEY
        actual = _API_KEY

        self.assertEquals(expected, actual, "apikey don't match: %s | %s"
            % (expected, actual))
    
    def test_javascript_timestamp(self):
        date='2011-11-11' 
        granularity='day'
        actual=javascript_timestamp(date,granularity)
        expected=1320969600000
        self.assertEquals(expected, actual, "js date converts don't match: %d | %d"
            % (expected, actual))

    def test_cw_search_keywords(self):
        keywords=['obama','economy']
        date_low='2011-11-11'
        date_high='2012-11-11'
        granularity='day'
        test_result=cw_search_keywords(keywords, date_low, date_high, granularity)
        actual=test_result[0]['results'][0]
        expected={'count': 0, 'day': 1320969600000}

        self.assertEquals(expected, actual, "first days in cw search do not match")

    def test_add_all(self):
        """still working on what this test will be! """
        keywords=['guns','economy']
        date_low='2011-11-17'
        date_high='2011-11-18'
        granularity='day'        
        API_KEY = _API_KEY
        api_results = []
        for keyword in keywords:
            query_params = {'apikey': API_KEY,
                        'phrase': keyword,
                        'start_date': date_low,
                        'end_date': date_high,
                        'granularity': granularity
                        }
            endpoint = 'http://capitolwords.org/api/dates.json'
            response = requests.get(endpoint, params=query_params)
            results = json.loads(response.text)
            results_entire_range = add_all(date_low, date_high, results, granularity="day")
            expected = {u'results': [{'count': 0, 'day': '2011-11-17'}, {'count': 0, 'day': '2011-11-18'}]}
            actual = results_entire_range
            self.assertEquals(expected, actual, "add missing dates not working")

if __name__ == '__main__':
    unittest.main()
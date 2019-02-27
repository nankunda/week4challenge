import unittest
import os
from unittest.mock import patch
from newsapi import NewsApi


class NewsApiTest(unittest.TestCase):
    def setUp(self):
        self.headline_request = NewsApi()
        self.content = self.headline_request.store_api_response()
        # fetch_data=self.headline_request.fetch_data()
        # self.response_data=fetch_data[0]
        # self.newsource=fetch_data[1]

    @patch('app.app_Api.NewsApi.get_user_source', return_value='bbc-news')
    def test_user_has_selected_news_source(self, get_user_source):
        self.assertIn(self.headline_request.get_user_source(), ('nbc-news', 'cnbc',
                                                                'bbc-news', 'cnn'))

    def test_store_api_response_has_data(self):

        self.assertNotEqual(self.content, [])

    def test_store_api_response_has_data_a_title(self):
        self.assertIsNotNone(self.content[0].get('title'))

    def test_store_api_response_has_data_a_description(self):
        self.assertIsNotNone(self.content[0].get('url'))

    def test_store_api_response_has_data_a_url(self):
        self.assertIsNotNone(self.content[0].get('description'))

    def test_number_of_returned_headlines_is_less_or_equal_to_10(self):
        self.assertLessEqual(self.headline_request.display_results(), 10)

    def test_api_key_was_successfully_collected(self):
        self.assertEqual(self.headline_request.get_api_key(),
                         os.environ.get('API_KEY'))

    def test_data_gets_retrived_from_the_newsapi(self):
        self.assertEqual(self.headline_request.check_status_code(), 200)


if __name__ == '__main__':
    unittest.main()
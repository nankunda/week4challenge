import requests
import inquirer
import os
import texttable as tt
from inquirer.themes import GreenPassion


class NewsApi:
    mynewssource = None

    def get_user_source(self):
        """"function for picking the news source from the user"""
        questions = [
            inquirer.List('sources',
                          message="From which news source would you like to acquire your headlines?",
                          choices=['nbc-news', 'cnbc',
                                   'bbc-news', 'cnn'],
                          ),


        ]
        """theme adds a green background to the items in the list"""
        answers = inquirer.prompt(questions, theme=GreenPassion())
        print("News Source : ", answers['sources'])
        self.mynewssource = answers['sources']
        return self.mynewssource

    def get_api_key(self):
        """function to retrieve a product key for the environment variable"""
        os.environ.get('API_KEY')
        if 'API_KEY' not in os.environ:
            raise ValueError(
                "Access Denied ..., you dont have a key in your environment variables, add api-key to your environment variables")
        return os.environ.get('API_KEY')

    def fetch_data(self):
        """function for collecting data for from the API"""
        if self.mynewssource:
            newssource = self.mynewssource
        else:
            newssource = "bbc-news"
        api_key = self.get_api_key()

        url = 'https://newsapi.org/v2/top-headlines?sources='+newssource + \
            '&apiKey='+api_key+'&pageSize=10'

        return (requests.get(url), newssource)

    def check_status_code(self):
        """function for checking whether the api call was successfull"""

        api_response, source = self.fetch_data()
        print("Status code:", api_response.status_code)
        if api_response.status_code == 200:
            print(
                "your query was successful, wait will we retrieve your data from", source)

        return api_response.status_code
    # function for storing the response for manipulation

    def store_api_response(self):
        """Function for storing the response data in json format"""
        data = self.fetch_data()
        api_response = (data[0]).json()

        headlineArticles = api_response.get('articles', [])

        return headlineArticles

    def display_results(self):
        """Function for diaplaying data to the user"""

        content = self.store_api_response()
        article_count = 1
        source_selected = self.mynewssource
        modifier = "="*110
        numberofitems = str(len(content))
        title = "TOP 10 HEADLINES FROM : "
        # creating the header for the display table.
        print('{} {} \n {} \n \t\t\t {} {} \n {}' .format('Headlines retrieved : ',
                                                          numberofitems, modifier, title, source_selected, modifier))

        """creating and styling the table"""
        tab = tt.Texttable()
        tab.set_cols_width([20, 85])
        tab.set_cols_align(["l", "l"])
        for article in content:
            # populating the display table
            row = ["Headline Count ", article_count]
            tab.add_row(row)
            row = ["TITLE : ",  article.get('title', "")]
            tab.add_row(row)
            row = ["DESCRIPTION: ",  article.get('description', "")]
            tab.add_row(row)
            row = ["URL: ",  article.get('url', "")]
            tab.add_row(row)
            row = ["",  ""]
            tab.add_row(row)
            article_count += 1

        s = tab.draw()
        print(s)
        return len(content)
import random
from datetime import datetime, timedelta
import json

import requests as rq
from bs4 import BeautifulSoup

from lib.settings import PROXIES, USER_AGENT_LIST
from lib.db_handler import HandleDB


class IndeedCrawler:
    def __init__(self):
        self.hdb_instance = HandleDB()
        self.http_session = rq.Session()

    def parse_result_list(self, response):
        """
        parse_result_list method to parse the index urls of job entries
        from search result page response.
        Args:
            response (requests.models.Response): http response object with
            html content and other info required to parse the page.

        Returns:
            List: job index urls list if successful, None otherwise.
        """
        try:
            soup = BeautifulSoup(response.content)
            job_params = {}
            job_list = soup.findAll('div', {'class': ['row', 'result']})
            for row_element in job_list:
                if 'jslast' not in row_element.get('class'):
                    job_params['source'] = 'indeed'
                    job_params['title'] = row_element.find(
                        'a', {'data-tn-element': 'jobTitle'}).get_text()
                    job_params['url'] = row_element.find(
                        'a', {'data-tn-element': 'jobTitle'}).get('href')
                    job_params['description'] = row_element.find(
                        'span', {'class': 'summary'}).get_text().strip()
                    job_params['job_type'] = 'N/A'
                    job_params['image'] = 'N/A'
                    location_list = row_element.find(
                        'span',
                        {'class': 'location'}).get_text().strip().split(',')
                    if len(location_list) == 1:
                        job_params['city'] = location_list[0]
                        job_params['state'] = location_list[0]
                    elif len(location_list) == 2:
                        job_params['city'] = location_list[0]
                        job_params['state'] = location_list[1]
                    job_params['how_to_apply'] = 'N/A'
                    job_params['author'] = row_element.find(
                        'span', {'class': 'company'}).get_text().strip()
                    date_string = row_element.find(
                        'span', {'class': 'date'})
                    if date_string is not None:
                        date_string = date_string.get_text().strip().split()[0]
                        if '+' not in date_string:
                            posted_at = datetime.today() - \
                                timedelta(days=int(date_string))
                            job_params['posted_at'] = posted_at
                        else:
                            job_params['posted_at'] = None
                    current_instance_job = self.hdb_instance.create_job(
                        **job_params)
                    if current_instance_job is not None:
                        print(current_instance_job.as_dict())

            current_page_index = soup.find(
                'div', {'class': 'pagination'}).find('b')
            if current_page_index is not None:
                next_page = current_page_index.find_next_sibling()
                if next_page is not None:
                    return 'https://www.indeed.com{}'.format(next_page.get('href'))
                else:
                    return None
            else:
                return None
        except Exception as error:
            print(error.message)
            return None

    def run(self):
        keyword_list = ['weed', 'marijuana', 'cannabis']
        for keyword in keyword_list:
            crawl_next_page = True
            seed_url = "https://www.indeed.com/jobs?q={}&start=0".format(
                keyword)
            self.http_session.headers['User-Agent'] = random.choice(
                USER_AGENT_LIST)
            response = None
            response = self.http_session.get(seed_url, proxies=PROXIES)
            next_page_url = self.parse_result_list(response)

            # iterating starting from seed url and fetching next
            # page url from the iterations
            while crawl_next_page:
                self.http_session.headers['User-Agent'] = random.choice(
                    USER_AGENT_LIST)
                print("[*]fetchin {}".format(next_page_url))
                response = self.http_session.get(
                    next_page_url, proxies=PROXIES)
                next_page_url = self.parse_result_list(response)
                if next_page_url is None:
                    crawl_next_page = False


if __name__ == '__main__':
    crawler_instance = IndeedCrawler()
    crawler_instance.run()

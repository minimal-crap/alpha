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
        self.indeed_seed_url = "https://www.indeed.com/jobs?as_and={}\
        &as_phr=&as_any=&as_not=&as_ttl=&as_cmp=&jt=all&st=&salary=\
        &radius=25&l=&fromage=15&limit=20&sort=date&psf=advsrch"

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
                    title_element = row_element.find(
                        'a', {'data-tn-element': 'jobTitle'})
                    if title_element is not None:
                        job_params['title'] = title_element.get_text()
                    else:
                        job_params['title'] = 'N/A'
                    job_params['url'] = 'http://www.indeed.com{}'.format(
                        row_element.find(
                            'a', {'data-tn-element': 'jobTitle'}).get('href'))
                    description_element = row_element.find(
                        'span', {'class': 'summary'})
                    if description_element is not None:
                        job_params['description'] = description_element.get_text(
                        ).strip()
                    else:
                        job_params['description'] = 'N/A'
                    job_params['job_type'] = 'N/A'
                    job_params['image'] = 'N/A'
                    location_list = row_element.find(
                        'span',
                        {'class': 'location'})
                    if location_list is not None:
                        location_list = location_list.get_text().strip().split(',')
                        if len(location_list) == 1:
                            job_params['city'] = location_list[0]
                            job_params['state'] = location_list[0]
                        elif len(location_list) == 2:
                            job_params['city'] = location_list[0]
                            job_params['state'] = location_list[1]
                    else:
                        job_params['city'] = 'N/A'
                        job_params['state'] = 'N/A'
                    job_params['how_to_apply'] = 'N/A'
                    company_element = row_element.find(
                        'span', {'class': 'company'})
                    if company_element is not None:
                        job_params['author'] = company_element.get_text().strip()
                    else:
                        job_params['author'] = 'N/A'
                    date_element = row_element.find(
                        'span', {'class': 'date'})
                    if date_element is not None:
                        date_string = date_element.get_text().lower()
                        # checking for jobs posted today
                        if date_string.find('today') != -1 or date_string.find(
                                'just posted') != -1:
                            job_params['posted_at'] = datetime.today()
                        else:
                            date_string = date_element.get_text().strip().split()[
                                0]
                        # for jobs posted later than today
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
            import ipdb
            ipdb.set_trace()
            print(error.message)
            return None

    def run(self):
        keyword_list = ['weed', 'marijuana', 'cannabis']
        for keyword in keyword_list:
            crawl_next_page = True
            self.http_session.headers['User-Agent'] = random.choice(
                USER_AGENT_LIST)
            response = None
            response = self.http_session.get(
                self.indeed_seed_url.format(keyword), proxies=PROXIES)
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

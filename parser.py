import json
import urllib
import requests
import time

from bs4 import BeautifulSoup as bs
from config import GOOGLE_SCHOLAR_DEFAULT_QUERY, GOOGLE_SCHOLAR_URL, GOOGLE_SCHOLAR_RESULTS_PER_PAGE, SOUP_DEFAULT_PARSER


def save_to_file(json_array):
    with open('result.json', 'w+', encoding='utf-8') as f:
        json.dump(
            json_array,
            f,
            ensure_ascii=False,
        )


def fetch_page_data(page, search_topic):
    results_offset = str(page * GOOGLE_SCHOLAR_RESULTS_PER_PAGE)
    url_params = urllib.parse.urlencode({
        **GOOGLE_SCHOLAR_DEFAULT_QUERY,
        'start':
        results_offset,
        'q':
        search_topic,
    })
    url = f"{GOOGLE_SCHOLAR_URL}?{url_params}"
    return requests.get(url)


def parse_page_soup(soup):
    parsed_data = []
    print(soup)
    for page_content in soup.find_all('div', {'id': 'gs_res_ccl_mid'}):

        for artcile_container in page_content.find_all(
                'div', {'class': 'gs_r gs_or gs_scl'}):
            for article in artcile_container.find_all('div',
                                                      {'class': 'gs_ri'}):
                arctile_data = {}

                for description in article.find_all('h3', {'class': 'gs_rt'}):
                    for links in description.find_all('a', href=True):
                        arctile_data["url"] = links['href']
                    arctile_data["title"] = description.text

                for authors in article.find_all('div', {'class': 'gs_a'}):
                    article_authors = []
                    for author in authors.find_all('a'):
                        article_authors.append(author.text)
                    arctile_data["authors"] = article_authors

                parsed_data.append(arctile_data)

    return parsed_data


def get_page_parsed_data(page_number, search_topic):
    data = fetch_page_data(page_number, search_topic)
    soup = bs(data.text, SOUP_DEFAULT_PARSER)

    # time.sleep(3)

    return parse_page_soup(soup)

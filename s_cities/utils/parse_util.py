
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from s_cities.utils import url_util
from s_cities.items import CountryItem, CityItem

from typing import AnyStr, Generator

def parse_continent(soup, request_url, continent_name=None):
    for h2 in soup.find_all('h2', attrs={'data-date': True}):
        if not h2.a: #skip some title without <a>
            print(request_url)
            continue
        country_dict = {}
        country_dict['country_icon'] = urljoin(request_url, h2.img['src'])
        country_dict['country_name'] = ' '.join(list(h2.a.stripped_strings))
        country_dict['country_url'] = urljoin(request_url, h2.a['href'])
        country_dict['country_description'] = h2.find_next_sibling('p').string
        country_dict['continent_name'] = continent_name
        yield country_dict


def parse_country_only_city(soup):
    table_list = soup.find_all('table')
    if table_list and len(table_list) >= 2:
        # Get Last Table, Cities&Towns
        for tr in table_list[-1].tbody.find_all('tr'):
            city_dict = {}
            city_dict['city_name'] = tr.find('td', class_='rname').span.string
            if tr.find('td', class_='rnative'):
                city_dict['city_native_name'] = tr.find('td', class_='rnative').string
            yield city_dict

def parse_country_contain_province(soup):
    table = soup.find('table', class_='data')
    tbody_admin1 = table.find_all('tbody', class_='admin1')
    tbody_admin2 = table.find_all('tbody', class_='admin2')
    state_list = [' '.join(state.find('td', class_='rname').stripped_strings) for state in tbody_admin1]
    city_list = [[' '.join(city_td.stripped_strings) for city_td in city_tbody.find_all('td', class_='rname')]
                 for city_tbody in tbody_admin2]
    for province,city_list in dict(zip(state_list, city_list)).items():
        for city in city_list:
            city_dict = {}
            city_dict['province_name'] = province
            city_dict['city_name'] = city
            yield city_dict


def parse_country(soup, request_url):
    table_list = soup.find_all('table')
    if table_list and len(table_list) >= 2:
        # Get Last Table, Cities&Towns
        for tr in table_list[-1].tbody.find_all('tr'):
            city_item = CityItem()
            city_item['city_name'] = tr.find('td', class_='rname').span.string
            city_item['city_native_name'] = tr.find('td', class_='rnative').string if tr.find('td', class_='rnative') \
                                            else None
            print(city_item)
            # yield city_item
    elif table_list and len(table_list) == 1:
        print('Another Table Style : {}'.format(request_url))
        pass
    else:
        print('Nokown {}'.format(request_url))
    pass

if __name__ == '__main__':
    # soup = BeautifulSoup(open('Africa.html'), 'lxml')
    # parse_continent(soup, 'https://www.citypopulation.de/Asia.html')
    # soup = BeautifulSoup(open('Afghanistan.html'), 'lxml')
    soup = BeautifulSoup(open('pakistan-admin.php'), 'lxml')
    # parse_country(soup, 'https://www.citypopulation.de/php/pakistan-admin.php')
    parse_country_contain_province(soup)
    pass
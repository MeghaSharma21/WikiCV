import json
from collections import defaultdict
import logging
import requests
import user_summary.constants as constants
import datetime
import math
import toolforge

logger = logging.getLogger('django')


# General function to call MediaWiki API and fetch data from it
def fetch_data_from_mediawiki_api(parameters):
    message = ''
    result = True
    json_data = {}
    url = 'https://en.wikipedia.org/w/api.php'
    response_object = requests.get(url, params=parameters)
    if response_object.status_code == 200:
        # Loading the response data into a dict variable
        json_data = json.loads(response_object.text)
        if 'error' in json_data:
            result = False
            message = 'Execution Failed at MediaWiki web service API,' \
                      + 'Error:' + str(json_data['error']['info'])
    else:
        # If response code is not ok
        result = False
        message = 'Execution Failed at MediaWiki web service API,' \
                  + 'HTTP Response Code: ' \
                  + str(response_object.status_code)

    return {"result": result, "message": message, "json_data": json_data}


# General function to assign datetime object to time filters
def evaluate_time_filters():
    filters_time_dict = {}
    for key, value in constants.TIME_FILTER_MAPPING.items():
        filters_time_dict[key] = \
            (datetime.datetime.today() - datetime.timedelta(value))
    return filters_time_dict


# Utility function to convert string into datetime object
def convert_string_to_datetime(date_string):
    return datetime.datetime.strptime(str(date_string), '%Y-%m-%dT%H:%M:%SZ')


# Function that uses MediaWiki API that maps page titles to IDs
def convert_titles_to_page_ids(titles):
    page_title_to_id_mapping = defaultdict(int)
    page_ids_results = []
    message = 'Page titles successfully converted to IDs.'
    success = True
    for i in range(math.ceil(len(titles) / 50)):
        # Since at max 50 titles can be passed in one request
        titles_list = ' | '.join(str(page) for page in
                                 titles[i * 50:(i + 1) * 50])

        parameters = {'action': 'query',
                      'format': 'json',
                      'prop': 'info',
                      'formatversion': 2,
                      'titles': titles_list}
        while True:
            results = fetch_data_from_mediawiki_api(parameters)
            if not results['result']:
                message = 'Error occurred while fetching page ' \
                          'IDs for titles. Results:'
                success = False
                break

            json_data = results['json_data']
            page_ids_results = \
                page_ids_results + json_data['query']['pages']

            if 'continue' in json_data:
                parameters['incontinue'] = \
                    json_data['continue']['incontinue']
                parameters['continue'] = \
                    json_data['continue']['continue']
            else:
                break

    logger.info(message)

    if not success:
        return -1
    else:
        for result in page_ids_results:
            page_title_to_id_mapping[str(result.get('pageid'))] = \
                str(result.get('title'))

        return page_title_to_id_mapping


# Function that evaluates time filters of Impact graph
def evaluate_time_filters_for_impact_graph():
    years = constants.YEAR_FILTER_FOR_IMPACT_GRAPH
    filters = []
    for i in years:
        for j in range(1, 13):
            filters.append(datetime.date(i, j, 1).strftime("%Y%m%d%H%M%S"))
    filters.append(datetime.date(years[-1] + 1, 1, 1).strftime("%Y%m%d%H%M%S"))
    return {"time_filters": filters, "year_filters": years}


# Function that takes PageAttributeTable object as input and converts
# it's fields into lists
def convert_page_attribute_table_objects_to_lists(page_attributes_data):
    page_views_dict = {}
    total_contribution_by_all_in_pages_dict = {}
    for data in page_attributes_data:
        page_views_dict[data.page_id] = data.page_views
        total_contribution_by_all_in_pages_dict[data.page_id] = \
            data.total_contribution_by_all_users
    return {"page_views_dict": page_views_dict,
            "total_contribution_by_all_in_pages_dict":
                total_contribution_by_all_in_pages_dict}


# Function to check whether user with input username exists or not
def check_user_exists(username):
    message = 'User with username:' + str(username) + 'exists'
    success = True
    try:
        conn = toolforge.connect('enwiki')
        with conn.cursor() as cursor:
            # finding how many users with the given username exist
            cursor.execute('SELECT count(*) FROM user WHERE user_name'
                           ' = %s ', [str(username)])
            result = cursor.fetchone()
            if result[0] == 0:
                success = False
                message = 'User with username:' + str(username) +\
                          ' does not exist'
    except Exception:
        message = 'Error fetching data from database for user: ' +\
                  str(username)
        success = False
    finally:
        cursor.close()
    conn.close()

    logger.info(message)
    return success

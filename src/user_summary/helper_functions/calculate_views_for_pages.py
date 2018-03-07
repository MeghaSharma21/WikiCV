import math
import logging
from collections import defaultdict
import user_summary.constants as constants
from user_summary.utility import fetch_data_from_mediawiki_api


logger = logging.getLogger('django')


# Function fetches page views of list of pages using MediaWiki API
def fetch_page_views(page_ids, pvip_days):
    page_views_results = []
    message = 'Page views calculated successfully. Results:'
    for i in range(math.ceil(len(page_ids) / 50)):
        # Since at max 50 IDs can be passed in one request
        page_ids_list = ' | '.join(str(page) for page in
                                   page_ids[i * 50:(i + 1) * 50])

        parameters = {'action': 'query',
                      'format': 'json',
                      'prop': 'pageviews',
                      'formatversion': 2,
                      'pvipdays': pvip_days,
                      'pageids': page_ids_list}
        while True:
            results = fetch_data_from_mediawiki_api(parameters)
            if not results['result']:
                message = 'Error occurred while fetching ' \
                          'page views. Results:'
                break

            json_data = results['json_data']
            page_views_results = \
                page_views_results + json_data['query']['pages']

            if 'continue' in json_data:
                parameters['pvipcontinue'] = \
                    json_data['continue']['pvipcontinue']
                parameters['continue'] = \
                    json_data['continue']['continue']
            else:
                break

    logger.info("{0}{1}".format(message, str(page_views_results)))
    if not results['result']:
        return -1
    else:
        return page_views_results


# Function to calculate page ID to views mapping for the user
def calculate_page_to_views_mapping(page_ids):
    message = 'Page to views mapping calculated successfully. ' \
              'Results:'
    pvip_days = constants.DEFAULT_PVIP_DAYS
    page_view_results = fetch_page_views(page_ids, pvip_days)
    page_to_view_mapping = defaultdict(int)

    if page_view_results == -1:
        message = 'Error occurred while calculating page to ' \
                  'views mapping. Results:'

    for result in page_view_results:
        for key, value in result.get('pageviews').items():
            if value is None:
                value = 0
            page_to_view_mapping[str(result.get('pageid'))] = \
                page_to_view_mapping[str(result.get('pageid'))] + value

    for key, value in page_to_view_mapping.items():
        page_to_view_mapping[key] = value/pvip_days

    logger.info("{0}{1}".format(message, str(page_to_view_mapping)))
    return page_to_view_mapping

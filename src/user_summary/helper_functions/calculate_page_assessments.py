import math
import logging
from collections import defaultdict
from user_summary.utility import fetch_data_from_mediawiki_api


logger = logging.getLogger('django')


# Function fetches assessments of a page using MediaWiki API
def calculate_page_assessments(page_ids):
    pages_assessment_results = []
    message = 'Page assessments calculated successfully. Results:'
    for i in range(math.ceil(len(page_ids) / 50)):
        # Since at max 50 IDs can be passed in one request
        page_ids_list = ' | '.join(str(page) for page in
                                   page_ids[i * 50:(i + 1) * 50])

        parameters = {'action': 'query',
                      'format': 'json',
                      'prop': 'pageassessments',
                      'palimit': '1',
                      'pageids': page_ids_list,
                      'formatversion': 2}

        while True:
            results = fetch_data_from_mediawiki_api(parameters)
            if not results['result']:
                message = 'Error occurred while fetching ' \
                          'page assessments. Results:'
                break

            json_data = results['json_data']
            pages_assessment_results = \
                pages_assessment_results + json_data['query']['pages']

            if 'continue' in json_data:
                parameters['pacontinue'] = \
                    json_data['continue']['pacontinue']
                parameters['continue'] = \
                    json_data['continue']['continue']
            else:
                break

    logger.info("{0}{1}".format(message, str(pages_assessment_results)))
    if not results['result']:
        return -1
    else:
        return pages_assessment_results


# Function calculates page to project mapping given page
# assessment results for pages
def calculate_page_to_project_mapping(pages_assessment_results):
    page_to_project_mapping = defaultdict(list)
    for assessment_result in pages_assessment_results:
        projects = []
        if assessment_result.get('pageassessments'):
            for key, value in assessment_result.get('pageassessments').items():
                projects.append(str(key))
        page_to_project_mapping[str(assessment_result.get('pageid'))] = \
            page_to_project_mapping[str(assessment_result.get('pageid'))] +\
            projects

    logger.info('Page to project mapping:{0}'
                .format(str(page_to_project_mapping)))
    return page_to_project_mapping

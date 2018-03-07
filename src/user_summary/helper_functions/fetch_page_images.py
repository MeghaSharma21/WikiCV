import math
import logging
from collections import defaultdict
from user_summary.utility import fetch_data_from_mediawiki_api

logger = logging.getLogger('django')


# Function fetches page images of list of pages using MediaWiki API
def fetch_page_images(page_ids):
    page_images_results = []
    success = True
    message = 'Page images fetched successfully. Results:'
    for i in range(math.ceil(len(page_ids) / 50)):
        # Since at max 50 IDs can be passed in one request
        page_ids_list = ' | '.join(str(page) for page in
                                   page_ids[i * 50:(i + 1) * 50])

        parameters = {'action': 'query',
                      'format': 'json',
                      'prop': 'pageimages',
                      'piprop': 'original',
                      'pageids': page_ids_list,
                      'formatversion': 2}
        while True:
            results = fetch_data_from_mediawiki_api(parameters)
            if not results['result']:
                message = 'Error occurred while fetching ' \
                          'page images. Results:'
                success = False
                break

            json_data = results['json_data']
            page_images_results = \
                page_images_results + json_data['query']['pages']

            if 'continue' in json_data:
                parameters['picontinue'] = \
                    json_data['continue']['picontinue']
                parameters['continue'] = \
                    json_data['continue']['continue']
            else:
                break

    logger.info("{0}{1}".format(message, str(page_images_results)))
    if not success:
        return -1
    else:
        return page_images_results


# Function to calculate page ID to images mapping for the user
def calculate_page_to_images_mapping(page_ids):
    message = 'Page to views mapping calculated successfully. ' \
              'Results:'
    page_images_results = fetch_page_images(page_ids)
    page_to_image_mapping = defaultdict(int)

    if page_images_results == -1:
        message = 'Error occurred while calculating page to ' \
                  'images mapping. Results:'

    for result in page_images_results:
        if result.get('original') is not None:
            page_to_image_mapping[str(result.get('pageid'))] = \
                (result.get('original')).get('source')
        else:
            page_to_image_mapping[str(result.get('pageid'))] = 'No image'

    logger.info("{0}{1}".format(message, str(page_to_image_mapping)))
    return page_to_image_mapping

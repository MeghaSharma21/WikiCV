from collections import defaultdict
from user_summary.helper_functions.calculate_views_for_pages \
    import calculate_page_to_views_mapping
from user_summary.helper_functions.fetch_page_images \
    import calculate_page_to_images_mapping
from user_summary.models import UserData, DataCache
from user_summary.utility import convert_titles_to_page_ids
import logging


# Class corresponds to Pinned Repository section
class PinnedRepositoryModule:

    logger = logging.getLogger('django')

    # Function to fetch stored pinned repositories of the user
    def get_repositories(self, username):
        message = 'Repositories successfully ' \
                  'fetched for user ' + str(username)
        repositories = defaultdict(int)
        if UserData.objects.filter(username=username).count() == 0:
            message = 'Data for user ' + str(username) +\
                      ' does not exist'
        else:
            page_ids = []
            user_data = UserData.objects.get(username=username)
            for key, value in user_data.pinned_repositories.items():
                page_ids.append(key)
                repositories[str(key)] = {'title': value['title'],
                                          'description':
                                              value['description']}

            page_to_views_mapping = \
                calculate_page_to_views_mapping(page_ids)

            cached_data = DataCache.objects.get(username=username)
            percentage_contribution = \
                cached_data.summary_content[
                    'percentageContributionInArticles']
            page_images = calculate_page_to_images_mapping(page_ids)

            for key, value in repositories.items():
                repositories[str(key)] = {'page_views':
                                          page_to_views_mapping[str(key)],
                                          'percentage_contribution':
                                          percentage_contribution[str(key)],
                                          'image': page_images[str(key)]}

        self.logger.info(message)
        return repositories

    # Function to update stored pinned repositories of the user
    def update_repositories(self, username, input_dict):
        message = 'Successfully updated pinned ' \
                  'repositories for the user.'
        data = {}
        titles = []
        success = True
        for key, value in input_dict['pinned_repositories'].items():
            titles.append(str(key))
        page_title_to_id_mapping = \
            convert_titles_to_page_ids(titles)
        if page_title_to_id_mapping == -1:
            message = 'Failed to update pinned ' \
                      'repositories for the user.'
            success = False
        else:
            for key, value in page_title_to_id_mapping.items():
                data[str(key)] = {'title': str(value),
                                  'description':
                                      str(input_dict['pinned_repositories']
                                          [str(value)])}
            input_dict['pinned_repositories'] = data
            UserData.update_or_create_object(username, input_dict)

        self.logger.info(message)
        return success

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
        user_repositories = []
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
                if key is not '':
                    user_repositories.append({'page_views':
                                              page_to_views_mapping[str(key)],
                                              'percentage_contribution':
                                              percentage_contribution[
                                                  str(key)],
                                              'image': page_images[str(key)],
                                              'title': value['title'],
                                              'description':
                                                  value['description']})
        self.logger.info(message)
        return user_repositories

    # Function to format pinned repositories of the user present in
    # the input data
    def format_input_repositories(self, username, input_dict):
        message = 'Successfully formatted input pinned ' \
                  'repositories for the user.'
        data = {}
        titles = []
        success = True
        error_message = ''
        cached_data = DataCache.objects.get(username=username)
        percentage_contribution = \
            cached_data.summary_content[
                'percentageContributionInArticles']
        for key, value in input_dict['pinned_repositories'].items():
            titles.append(str(key))
        page_title_to_id_mapping = \
            convert_titles_to_page_ids(titles)
        if page_title_to_id_mapping == -1:
            message = 'Failed to format input pinned ' \
                      'repositories for the user.'
            success = False
        else:
            for key, value in page_title_to_id_mapping.items():
                if key not in percentage_contribution:  # If user hasn't
                                                        # contributed to
                                                        # the repository
                    error_message = 'You have not contributed to ' +\
                              str(value) +\
                              'article. Hence, you can not pin it.'
                    self.logger.info(error_message)

                data[str(key)] = {'title': str(value),
                                  'description':
                                      str(input_dict['pinned_repositories']
                                          [str(value)])}
            input_dict['pinned_repositories'] = data
        if not success:
            input_dict['pinned_repositories'] = data
        self.logger.info(message)
        return {'input_dict': input_dict,
                'error_message': error_message}

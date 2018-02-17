from django.db import models
from jsonfield import JSONField
import user_summary.constants as constants


# Model for table that contains the cached data for every user
class DataCache(models.Model):
    username = models.CharField(max_length=50, primary_key=True)
    summary_content = JSONField()
    achievements_content = JSONField()
    contribution_content = JSONField()
    page_to_project_mapping = JSONField()
    updated_at = models.DateTimeField(auto_now=True)

    # Method to create a new entry in the table
    @staticmethod
    def create_object(username, data):
        DataCache.objects.create(username=username,
                                 summary_content=data['summary_content'],
                                 achievements_content=data[
                                     'achievements_content'],
                                 contribution_content={
                                     'edits_array': data['edits_array'],
                                     'articles_created_array':
                                         data['articles_created_array']},
                                 page_to_project_mapping=data[
                                     'page_to_project_mapping'])

    # Method to update or create (in case it isn't present earlier)
    #  an entry in the table
    @staticmethod
    def update_or_create_object(username, data):
        DataCache.objects.update_or_create(username=username, defaults={
            'summary_content':
                data['summary_content'],
            'achievements_content':
                data['achievements_content'],
            'contribution_content':
                {'edits_array': data['edits_array'],
                 'articles_created_array':
                     data['articles_created_array']},
            'page_to_project_mapping':
                data['page_to_project_mapping']})


class WikipediaGeneralDataCache(models.Model):
    id = models.IntegerField(primary_key=True)
    updated_at = models.DateTimeField(auto_now=True)
    contribution_distribution = JSONField()

    @staticmethod
    def create_object(contribution_distribution):
        WikipediaGeneralDataCache.objects\
            .create(id=constants.GENERAL_DATA_CACHE_DEFAULT_ID,
                    contribution_distribution=contribution_distribution)

    @staticmethod
    def update_or_create_object(contribution_distribution):
        WikipediaGeneralDataCache.objects\
            .update_or_create(id=constants.GENERAL_DATA_CACHE_DEFAULT_ID,
                              defaults={'contribution_distribution':
                                        contribution_distribution})

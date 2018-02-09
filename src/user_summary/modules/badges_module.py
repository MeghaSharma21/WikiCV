import dateutil.parser
from dateutil.relativedelta import relativedelta
import logging


# Contains data and functions related to the badges section of WikiCV
class BadgesModule:
    # Get an instance of a logger
    logger = logging.getLogger('django')
    badges = []

    # Function calculates badges for the user
    def badgesStarterFunction(self, editSummary, userInfo):
        yearBadge = self._assignYearBadge(editSummary['userId'],
                                          editSummary[
                                              'firstContributionTimestamp'],
                                          editSummary[
                                              'lastContributionTimestamp'])
        if yearBadge:
            self.badges.append([str(yearBadge[0]) + '+ Years', yearBadge[1]])

        bytesAddedBadge = \
            self._assignBytesAddedBadge(editSummary['userId'],
                                        editSummary['bytesAdded'])
        if bytesAddedBadge:
            self.badges.append([str(bytesAddedBadge[0]) +
                                '+ MB added', bytesAddedBadge[1]])

        specialRightsBadge = \
            self._assignSpecialRightsBadge(editSummary['userId'],
                                           userInfo['specialGroups'])
        if specialRightsBadge:
            self.badges.append([specialRightsBadge[0], specialRightsBadge[1]])

    # Function assigns badge for being active for x+ years
    def _assignYearBadge(self, userId, firstContributionTimestamp,
                         lastContributionTimestamp):
        yearBucket = [[1, 'bronze'], [3, 'silver'], [5, 'gold']]
        badge = []
        if firstContributionTimestamp and lastContributionTimestamp:
            activeTimePeriod = relativedelta(dateutil.parser.parse
                                             (firstContributionTimestamp),
                                             dateutil.parser.parse
                                             (lastContributionTimestamp)).years
            for threshold in yearBucket:
                if activeTimePeriod > threshold[0]:
                    badge = threshold
                    self.logger.info('User {0}has been active for {1}years. '
                                     'Hence got {2}badge.'
                                     .format(str(userId),
                                             str(activeTimePeriod),
                                             str(badge)))
        return badge

    # Function assigns badge for adding x MB+ bytes
    def _assignBytesAddedBadge(self, userId, bytesAdded):
        bytesBucket = [[1, 'bronze'], [10, 'silver'], [50, 'silver'],
                       [100, 'gold'], [200, 'gold']]
        badge = []
        if bytesAdded:
            for threshold in bytesBucket:
                if bytesAdded/100000 > threshold[0]:
                    badge = threshold
                    self.logger.info(
                        "User {0}has added {1}bytes. Hence, got {2}badge."
                        .format(str(userId), str(bytesAdded), str(badge)))
        return badge

    # Function assigns badge for having special rights.
    # For now, only Admin badge has been introduced.
    def _assignSpecialRightsBadge(self, userId, specialGroups):
        badge = []
        if specialGroups and 'sysop' in specialGroups:
            badge = ['Admin', 'gold']
            self.logger.info('User {0}is an admin. Hence, got {1}badge.'
                             .format(str(userId), str(badge)))
        return badge

import dateutil.parser
from dateutil.relativedelta import relativedelta
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Function calculates badges for the user
def assignBadges(userId, firstContributionTimestamp, lastContributionTimestamp,
                 bytesAdded, specialGroups):
    badges = []
    yearBadge = assignYearBadge(userId, firstContributionTimestamp,
                                lastContributionTimestamp)
    if yearBadge:
        badges.append([str(yearBadge[0]) + '+ Years', yearBadge[1]])

    bytesAddedBadge = assignBytesAddedBadge(userId, bytesAdded)
    if bytesAddedBadge:
        badges.append([str(bytesAddedBadge[0]) +
                      '+MB added', bytesAddedBadge[1]])

    specialRightsBadge = assignSpecialRightsBadge(userId, specialGroups)
    if specialRightsBadge:
        badges.append([specialRightsBadge[0], specialRightsBadge[1]])
    return badges


# Function assigns badge for being active for x+ years
def assignYearBadge(userId, firstContributionTimestamp,
                    lastContributionTimestamp):
    yearBucket = [[1, 'bronze'], [3, 'silver'], [5, 'gold']]
    badge = []
    if firstContributionTimestamp and lastContributionTimestamp:
        activeTimePeriod = relativedelta(dateutil.parser
                                         .parse(firstContributionTimestamp),
                                         dateutil.parser
                                         .parse(lastContributionTimestamp)
                                         ).years
        for threshold in yearBucket:
            if activeTimePeriod > threshold[0]:
                badge = threshold
                logger.info('User ' + str(userId) + 'has been active for ' +
                            str(activeTimePeriod) + 'years. Hence got ' +
                            str(badge) + 'badge.')
    return badge


# Function assigns badge for adding x MB+ bytes
def assignBytesAddedBadge(userId, bytesAdded):
    bytesBucket = [[1, 'bronze'], [10, 'silver'], [50, 'silver'],
                   [100, 'gold'], [200, 'gold']]
    badge = []
    if bytesAdded:
        for threshold in bytesBucket:
            if bytesAdded/100000 > threshold[0]:
                badge = threshold
                logger.info('User ' + str(userId) + 'has added ' +
                            str(bytesAdded) + 'bytes. Hence, got ' +
                            str(badge) + 'badge.')
    return badge


# Function assigns badge for having special rights.
# For now, only Admin badge has been introduced.
def assignSpecialRightsBadge(userId, specialGroups):
    badge = []
    if specialGroups:
        if 'sysop' in specialGroups:
            badge = ['Admin', 'gold']
            logger.info('User ' + str(userId) + 'is an admin. Hence, got ' +
                        str(badge) + 'badge.')
    return badge

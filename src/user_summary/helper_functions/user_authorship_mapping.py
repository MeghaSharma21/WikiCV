import toolforge
import logging

# Get an instance of a logger
logger = logging.getLogger('django')


# Function calculates authorship of the user in
# every article he/she has contributed
def calculateUserAuthorishipMapping(pagesContributed, userId):
    message = 'Authorship calculated Successfully for all articles'
    result = True
    if len(pagesContributed) > 0:
        # Dictionary which will map pageId and contributions to it
        contributionByAll = {}
        contributionByUsername = {}
        # Dictionary which will map articleId and
        # percentage contribution to it by username
        percentageContribution = {}
        pages = ', '.join(str(page) for page in pagesContributed)
        try:
            conn = toolforge.connect('enwiki')
            with conn.cursor() as cursor:
                cursor.execute("SELECT A.rev_page, SUM(ABS(A.rev_len - "
                               "(CASE WHEN A.rev_id=B.rev_id THEN 0 "
                               "ELSE ABS(B.rev_len) END))), SUM(ABS("
                               "(CASE WHEN A.rev_user = %s "
                               "THEN ABS(A.rev_len) "
                               "ELSE 0 END) - "
                               "(CASE WHEN A.rev_user = %s THEN "
                               "(CASE WHEN A.rev_id=B.rev_id THEN 0 "
                               "ELSE ABS(B.rev_len) END) ELSE 0 END))) "
                               "FROM revision A, revision B WHERE A.rev_page "
                               "IN (%s) AND MOD(A.rev_deleted,2) = 0 AND "
                               "(B.rev_id = CASE A.rev_parent_id WHEN 0 "
                               "THEN A.rev_id ELSE A.rev_parent_id END) "
                               "GROUP BY A.rev_page"
                               % (str(userId), str(userId), pages))
                results = cursor.fetchall()
            for result in results:
                contributionByAll[result[0]] = result[1]
                contributionByUsername[result[0]] = result[2]
            for page in pagesContributed:
                percentageContribution[page] = \
                    (contributionByUsername[page]*100)/contributionByAll[page]
            result = True
        except Exception as e:
            message = 'Exception occured while establishing' \
                      + 'connection with database for calculating' \
                      + 'user-authorship mapping. Exception: ' + str(e)
            result = False
        finally:
            cursor.close()
            conn.close()
    else:
        message = 'The user does not have any contributions. Hence,'
        + 'can not calculate user-authorship mapping'
        result = False
    logger.info(message)
    return {'percentageContribution': percentageContribution,
            'result': result}

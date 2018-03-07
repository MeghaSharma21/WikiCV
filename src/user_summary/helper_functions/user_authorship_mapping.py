import toolforge
import logging

# Get an instance of a logger
from user_summary.utility import evaluate_time_filters_for_impact_graph

logger = logging.getLogger('django')


# Function calculates authorship of the user in
# every article he/she has contributed
def calculateUserAuthorishipMapping(pagesContributed, userId):
    message = 'Authorship calculated Successfully for all articles'
    success = True
    if len(pagesContributed) > 0:
        # Dictionary which will map pageId and contributions to it
        contributionByAll = {}
        contributionByUsername = {}
        # Dictionary which will map articleId and
        # percentage contribution to it by username
        percentageContribution = {}
        filters = \
            evaluate_time_filters_for_impact_graph()
        time_filters = filters["time_filters"]
        year_filters = filters["year_filters"]
        user_contribution_based_on_time = {}
        pages = ', '.join(str(page) for page in pagesContributed)
        try:
            conn = toolforge.connect('enwiki')
            with conn.cursor() as cursor:
                query = "SELECT A.rev_page, SUM(ABS(A.rev_len - " \
                        "(CASE WHEN A.rev_id=B.rev_id THEN 0 ELSE " \
                        "ABS(B.rev_len) END))),SUM(ABS((CASE WHEN " \
                        "A.rev_user = %s THEN ABS(A.rev_len) ELSE " \
                        "0 END) - (CASE WHEN A.rev_user = %s THEN " \
                        "(CASE WHEN A.rev_id=B.rev_id THEN 0 ELSE " \
                        "ABS(B.rev_len) END) ELSE 0 END))), %s  " \
                        "FROM revision A, revision B WHERE A.rev_page " \
                        "IN (%s) AND MOD(A.rev_deleted,2) = 0 AND " \
                        "(B.rev_id = CASE A.rev_parent_id WHEN 0 THEN " \
                        "A.rev_id ELSE A.rev_parent_id END) GROUP BY " \
                        "A.rev_page" % \
                        (str(userId), str(userId), ', '
                         .join((len(time_filters)-1) *
                               ["SUM(CASE WHEN ((A.rev_timestamp >= %s) "
                                "AND (A.rev_timestamp < %s) AND "
                                "(A.rev_user = %s)) THEN ABS(A.rev_len - "
                                "(CASE WHEN A.rev_id=B.rev_id THEN 0 ELSE "
                                "ABS(B.rev_len) END)) ELSE 0 END)"]), pages)
                params = []
                for index in range(len(time_filters) - 1):
                    params.append(time_filters[index])
                    params.append(time_filters[index + 1])
                    params.append(str(userId))
                cursor.execute(query, params)
                results = cursor.fetchall()

            # Initializing nested dictionary for
            # user_contribution_based_on_time
            for i in range(len(year_filters)):
                user_contribution_based_on_time[year_filters[i]] = {}
                for j in range(0, 12):
                    user_contribution_based_on_time[year_filters[i]][j] = {}

            for result in results:
                contributionByAll[result[0]] = result[1]
                contributionByUsername[result[0]] = result[2]
                # Making nested dictionary for user_contribution_based_on_time.
                # It's first level of nesting is for year, then for month and
                # lastly for the page_id to which the user has contributed.
                for i in range(len(year_filters)):
                    for j in range(0, 12):
                        user_contribution_based_on_time[year_filters[i]][j][
                            result[0]] = result[12 * i + j + 3]
            for page in pagesContributed:
                percentageContribution[str(page)] = \
                    (contributionByUsername[page] * 100)\
                    / contributionByAll[page]
        except Exception as e:
            message = 'Exception occurred while establishing ' \
                      + 'connection with database for calculating ' \
                      + 'user-authorship mapping. Exception: ' + str(e)
            success = False
        finally:
            cursor.close()
            conn.close()
    else:
        message = 'The user does not have any contributions. Hence, ' \
                  'can not calculate user-authorship mapping'
        success = False
    logger.info(message)
    return {'percentageContribution': percentageContribution,
            'total_contribution': contributionByAll,
            'user_contribution_based_on_time':
                user_contribution_based_on_time,
            'result': success}

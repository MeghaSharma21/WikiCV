import toolforge
import logging
import user_summary.constants as constants

logger = logging.getLogger('django')


# Function that bucketizes users based on contributions
def calculate_users_contribution_distribution():
    message = 'Contribution distribution calculated successfully ' \
              'for all users. Results:'
    success = True
    # Definition of 8 groups - list of groups - (lowerlimit, upperlimit) pair -
    # both inclusive
    groups = constants.CONTRIBUTION_BUCKETS
    params = []
    for group in groups:
        params.append(group[0])
        params.append(group[1])
    query = "SELECT COUNT(*), SUM(user_editcount>0), %s FROM user" \
            % (', '.join(len(groups)*["SUM(user_editcount >= %s AND "
                                      "user_editcount <= %s)"]))
    try:
        conn = toolforge.connect('enwiki')
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            result = cursor.fetchone()
    except Exception:
        success = False
        message = 'Error occurred while calculating contribution' \
                  ' distribution for all users. Results:'
    finally:
        cursor.close()
        conn.close()
    if success:
        total_no_of_users = result[0]
        # calculating percentage of users lying in different ranges
        # percentage_of_users_in_group[i] contains percentage of users
        # in ith group
        percentage_of_users_in_group = [0] * (len(groups) + 1)
        for i in range(1, len(percentage_of_users_in_group)):
            percentage_of_users_in_group[i] = \
                round(100 * (result[i] / total_no_of_users), 2)

    logger.info("{0}{1}".format(message, str(percentage_of_users_in_group)))
    return {'success': success,
            'percentage_of_users_in_group': percentage_of_users_in_group,
            'total_no_of_users': total_no_of_users}

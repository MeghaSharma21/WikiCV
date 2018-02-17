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
    try:
        conn = toolforge.connect('enwiki')
        with conn.cursor() as cursor:
            cursor.execute(
                'SELECT COUNT(*), SUM(user_editcount>0), '
                'SUM(user_editcount >= %s AND user_editcount <= %s), '
                'SUM(user_editcount >= %s AND user_editcount <= %s), '
                'SUM(user_editcount >= %s AND user_editcount <= %s), '
                'SUM(user_editcount >= %s AND user_editcount <= %s), '
                'SUM(user_editcount >= %s AND user_editcount <= %s), '
                'SUM(user_editcount >= %s AND user_editcount <= %s), '
                'SUM(user_editcount >= %s AND user_editcount <= %s), '
                'SUM(user_editcount >= %s) FROM user',
                [groups[0][0], groups[0][1], groups[1][0], groups[1][1],
                 groups[2][0], groups[2][1], groups[3][0], groups[3][1],
                 groups[4][0], groups[4][1], groups[5][0], groups[5][1],
                 groups[6][0], groups[6][1], groups[7][0]])
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

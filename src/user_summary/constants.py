import datetime
# File contains constants for user_summary app

# Mapping of time filter with their time equivalent
TIME_FILTER_MAPPING = {'7 days': 7, '15 days': 15, '1 month': 30,
                       '4 months': 120, '8 months': 240,
                       '1 year': 365, '2 years': 365 * 2,
                       '3 years': 365 * 3}

# Mapping of time filter with their time equivalent for Impact graph
IMPACT_GRAPH_TIME_FILTER_MAPPING = {'1 year': 365, '2 years': 365 * 2,
                                    '3 years': 365 * 3}

# Default ID for WikipediaGeneralDataCache table
GENERAL_DATA_CACHE_DEFAULT_ID = 1

# Groups in which users are divided based on their contributions
CONTRIBUTION_BUCKETS = [(0, 0), (1, 1), (2, 10), (11, 50), (51, 100),
                        (100, 500), (501, 1000), (1001, 2147483648)]

# Default value for no. of days for which page views need
# to be calculated
DEFAULT_PVIP_DAYS = 60

# Default threshold for contribution by user in one page
DEFAULT_CONTRIBUTION_THRESHOLD = 15

# Default threshold for contribution by user in one page for
# achievements
DEFAULT_CONTRIBUTION_THRESHOLD_FOR_ACHIEVEMENTS = 25

# Array of year filters for impact graph
YEAR_FILTER_FOR_IMPACT_GRAPH = [datetime.datetime.now().year - 2,
                                datetime.datetime.now().year - 1,
                                datetime.datetime.now().year]

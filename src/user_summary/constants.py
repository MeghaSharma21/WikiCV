# File contains constants for user_summary app

# Mapping of time filter with their time equivalent
TIME_FILTER_MAPPING = {'1 hour': 1 / 24, '6 hours': 6 / 24,
                       '12 hours': 12 / 24, '1 day': 1,
                       '7 days': 7, '15 days': 15, '1 month': 30,
                       '4 months': 120, '8 months': 240,
                       '1 year': 365, '2 years': 365 * 2,
                       '3 years': 365 * 3}

# Default ID for WikipediaGeneralDataCache table
GENERAL_DATA_CACHE_DEFAULT_ID = 1

# Groups in which users are divided based on their contributions
CONTRIBUTION_BUCKETS = [(0, 0), (1, 1), (2, 10), (11, 50), (51, 100),
                        (100, 500), (501, 1000), (1001, 2147483648)]

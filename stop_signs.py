import pandas as pd
from sodapy import Socrata
import geojson
from pprint import pprint

# Unauthenticated client only works with public data sets. Note 'None'
# in place of application token, and no username or password:
client = Socrata("data.sfgov.org", None)

# Example authenticated client (needed for non-public datasets):
# client = Socrata(data.sfgov.org,
#                  MyAppToken,
#                  userame="user@example.com",
#                  password="AFakePassword")

# First 2000 results, returned as JSON from API / converted to Python list of
# dictionaries by sodapy.
results = client.get("4542-gpa3", limit=2000)

# Convert to pandas DataFrame
results_df = pd.DataFrame.from_records(results)

potrero_intersection = results_df.loc[(results_df.street == 'MARIPOSA')
                                      & (results_df.x_street == 'HARRISON')]
hunterspoint_intersection = results_df.loc[results_df.street == 'DONAHUE']

for p in potrero_intersection.point:
    print(p)
for p in hunterspoint_intersection.point:
    print(p)

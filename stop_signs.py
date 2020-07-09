import pandas as pd
from sodapy import Socrata
import sys
import getopt


def main(argv):
    streetname = ''
    x_streetname = ''
    try:
        opts, args = getopt.getopt(argv, "hs:x:", ["street=", "xstreet="])
    except getopt.GetoptError:
        print("stop_signs.py -s <street> optional:-x <xstreet>")
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print("stop_signs.py -s <street> optional:-x <xstreet>")
            sys.exit()
        elif opt in ("-s", "--street"):
            streetname = arg
        elif opt in ("-x", "--xstreet"):
            x_streetname = arg

    if streetname == '':
        print("Need a valid streetname")
        sys.exit()

    # Unauthenticated client only works with public data sets. Note 'None'
    # in place of application token, and no username or password:
    client = Socrata("data.sfgov.org", None)

    # Example authenticated client (needed for non-public datasets):
    # client = Socrata(data.sfgov.org,
    #                  MyAppToken,
    #                  userame="user@example.com",
    #                  password="AFakePassword")

    # First 2000 results, returned as JSON from API / converted to Python list
    # of dictionaries by sodapy.
    results = client.get("4542-gpa3", limit=2000)

    # Convert to pandas DataFrame
    results_df = pd.DataFrame.from_records(results)

    if x_streetname != '':
        intersection = results_df.loc[(results_df.street == streetname)
                                      & (results_df.x_street == x_streetname)]
    else:
        intersection = results_df.loc[results_df.street == streetname]

    for _, row in intersection.iterrows():
        print("===================================")
        print(row.street + " X " + row.x_street)
        print(row.direction, row.st_facing)
        print(row.point)


if __name__ == "__main__":
    main(sys.argv[1:])

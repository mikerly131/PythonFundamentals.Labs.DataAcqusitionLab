""" Script to get all of the data from NOAA API """

# Limit must be passed with GET call, max is 1000, need to figure out header or somewhere else
# Offset should be reset each GET call and included in GET call, need to figure out header or somewhere else
# Each call data is json and should be dumped into json files, saved in data director in project
# import utillib.request
# will get a count of the total number of rows of data to grab in first call, stays same each call it seems

# So far able to call the API with my token and get the JSON response
import urllib.request
import json
import math

# Will be using offset and limit parameter arugments when making calls to get next series of data as json.
offset = 1
limit = 5
url = f"https://www.ncdc.noaa.gov/cdo-web/api/v2/locations?offset={offset}&limit={limit}"
token = "zVpLmzmWOkYHFZDidWkqSgCcCIqaoUMS"
req = urllib.request.Request(url=url)
req.add_header('token', token)

# All of this to get the total count of records the API can serve up and then use that as counter for calls to make
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read())
    count = data['metadata']['resultset']['count']

# Each call will get up to 1000 rows, so
raw_calls = count / 1000
api_calls = math.ceil(raw_calls)

# Loop to make api calls write json files
for call in range(0, api_calls):
    if call == 0:
        offset = 0
    else:
        offset = (1000 * call) + 1
    limit = 1000
    url = f"https://www.ncdc.noaa.gov/cdo-web/api/v2/locations?offset={offset}&limit={limit}"
    token = "zVpLmzmWOkYHFZDidWkqSgCcCIqaoUMS"
    req = urllib.request.Request(url=url)
    req.add_header('token', token)

    # Call API and collect the data in json format from the api response
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read())

    # Write each group of 1000 records, or a call, to a file with incrementing call number
    j_file = f'data/locations_{call}.json'
    with open(j_file, 'w') as json_file:
        json.dump(data, json_file)
        json_file.close()

    print(f'Created file for call {call}.')

# This function takes a while to run

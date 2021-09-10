from datetime import datetime, timedelta
from daily_worker import read_from_s3_bucket
import yaml
import json
import requests


if __name__ == "__main__":
    print("Sync APIs with yesterdays job advertisements")

    # get yesterday's date:
    yesterday = datetime.now() - timedelta(days=1)
    yesterday_date = yesterday.strftime('%Y-%m-%d')
    print("Yesterday's Date:", yesterday_date)

    # read today's, data from s3 bucket
    s3_url = 'https://jobfeed-assignment-data.s3.eu-west-1.amazonaws.com/Jobs.' + yesterday_date + '.0.xml'
    active_jobs_for_yesterday = read_from_s3_bucket(str(s3_url))

    # upload all new job advertisements
    response = requests.post('https://httpbin.org/post', data=json.dumps(active_jobs_for_yesterday))
    if response.status_code == 200:
        print('Updated Date on the API endpoint for yesterday')
    else:
        # probably could use retries
        print('Failed to sync data with the API endpoint')


    # post latest date records to yaml file
    file = open('previous_jobs.yaml', 'w+')
    yaml.dump(active_jobs_for_yesterday, file)

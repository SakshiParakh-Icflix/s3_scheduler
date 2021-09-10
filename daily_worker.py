from urllib.request import urlopen
from datetime import datetime
import xmltodict
import requests
import json
import yaml


def read_from_s3_bucket(s3_url):
    try:
        # download the xml file
        file = urlopen(s3_url)
        data = file.read()
        file.close()
        return json.loads(json.dumps(xmltodict.parse(data)))
    except:
        print("Something wrong with connecting to the S3 bucket! Please try again later")



def upload_jobs_to_external_api(active_jobs_for_today):
    # get jobs from the previous day and compare for new jobs
    # 1. use persistant storage to store everyday data
    # 2. save only last days data to YAML
    new_jobs = []

    # get previous records from yaml file
    file = open('previous_jobs.yaml', 'r')
    previous_jobs = yaml.load(file)

    if(previous_jobs != None):
        # compare jobs
        previous_jobs_source_urls = {(j['source_url']) for j in previous_jobs['Jobs']['Job']}
        for j in active_jobs_for_today['Jobs']['Job']:
            if (j['source_url']) not in previous_jobs_source_urls:
                    # its a new job
                    new_jobs.append(j)

    else:
        # all jobs are new
        new_jobs = active_jobs_for_today['Jobs']['Job']

    # if new records
    if(new_jobs != []):
        # post new jobs to external api
        response = requests.post('https://httpbin.org/post', data={'Jobs': {'Job': new_jobs}})
        if response.status_code == 200:
            print('Successful update of new data ')
        else:
            print('Failed to sync data with the API endpoint')

    # post latest date records to yaml file
    file = open('previous_jobs.yaml', 'w+')
    yaml.dump(active_jobs_for_today, file)



def delete_jobs_from_external_api(active_jobs_for_today):
    non_existing_jobs = []

    # get previous records from yaml file
    file = open('previous_jobs.yaml', 'r')
    previous_jobs = yaml.load(file)

    if (previous_jobs != None):
        # delete jobs that exist in the previous days records but not in the current date
        active_jobs_source_urls = {(j['source_url']) for j in active_jobs_for_today['Jobs']['Job']}
        for j in previous_jobs['Jobs']['Job']:
            if (j['source_urls']) not in active_jobs_source_urls:
                    # its a non exsistent job
                    non_existing_jobs.append(j)

        if non_existing_jobs != []:
            # delete from the api
            response = requests.delete('https://httpbin.org/delete', data={'Jobs': {'Job': non_existing_jobs}})
            if response.status_code == 200:
                print('Successful delete of non existing data ')
            else:
                print('Failed to sync data with the API endpoint')
    else:
        # no data to delete
        pass



if __name__ == "__main__":
    print("Daily Task to synchronize jobs advertizement from S3")

    # get today's date:
    current_date = datetime.today().strftime('%Y-%m-%d')
    print("Current Date:", current_date)

    # read today's, data from s3 bucket
    s3_url = 'https://jobfeed-assignment-data.s3.eu-west-1.amazonaws.com/Jobs.' + current_date + '.0.xml'
    active_jobs_for_today = read_from_s3_bucket(str(s3_url))

    # upload new job advertisements
    upload_jobs_to_external_api(active_jobs_for_today)
    
    # delete non exsiting advertizements
    delete_jobs_from_external_api(active_jobs_for_today)

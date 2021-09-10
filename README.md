# s3_scheduler
# About
  The application runs a daily task to syncronize data from an S3 bucket 
  and an external REST API

# Steps to run the application
  Step 1: build a docker image 
  
  ```docker build -t job-syncer .```
  
  step 2: run the the docker image
  
  ```docker run -it --rm job-syncer```
  
          The docker image runs a script to: 
          i) load prerequisite libraries from 
          ii) load yesterday's data and 
          iii) run a cron job to sync data daily from that day onwards

# IMPORTANT NOTICE
    should  have used chunk and chunk-size to split the large XML file
    and sync data chunk by chunk
     
    couldn't get to it because of time constraint.
    
# Another tried Appraoch
    One could also use AWS Lamda to create a python function and 
    add AWS cloud watch to add an event rule for running the function daily

# untried Approach
             


                

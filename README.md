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
    add AWS cloud watch to add an event rule for running the function daily. 
    AWS lamda is useful to reduce compute time
    
    Step 1: Create a Lamda function
    Step 2: If needed Add Api Gateway trigger (to get an HTTP or REST API ); 
    if you want to expose the app
    Step 3: create a zip file of your code and in the upload section add the file
    Step 4: write a lambda_function.py which has the lambda handler
    that calls our main function 
    
    ```
    import json
    from s3_scheduler import daily_worker
    
    def lambda_handler(event, context):
        daily_worker.main()
        
    return {
        'statusCode': 200,
    }
    ``` 
    
    Step 5: create an AWS CloudWatch by going in rules and creating an event;
    schedule the event for daily once
    
    Step 6: add the lambda function you created to the rule 
    Step 7: you can use cloud watch logger to see the events being fired.
    Step 8: deploy and test your code

# untried Approach
    figured that the task could also be done using elasticbeanstalk, 
    but don't have any experience with it       

# Automated Deployment
    this is we wanted to have continous push and continious deployment through github
    add .github folder -> workflows -> docker-image.yaml file
    
    ```
    name: Publish Docker image
    on:
      release:
        types: [published]
    jobs:
      push_to_registry:
        name: Push Docker image to Docker Hub
        runs-on: ubuntu-latest
        steps:
          - name: Check out the repo
            uses: actions/checkout@v2
          - name: Push to Docker Hub
            uses: docker/build-push-action@v1
            with:
              username: ${{ secrets.DOCKER_USERNAME }}
              password: ${{ secrets.DOCKER_PASSWORD }}
              repository: <DOCKER USERNAME>/<DOCKER REPOSITORY>
              tag_with_ref: true

    ```
                

# Third-party imports...
from nose.tools import assert_true
import requests


def test_api_post_request_response():
    # Send a request to the API server and store the response.
    # check API endpoint is healthy
    response = requests.post('https://httpbin.org/post')

    # Confirm that the request-response cycle completed successfully.
    assert_true(response.ok)


def test_api_delete_request_response():
    # Send a request to the API server and store the response.
    # check API endpoint is healthy
    response = requests.delete('https://httpbin.org/delete')

    # Confirm that the request-response cycle completed successfully.
    assert_true(response.ok)


def test_s3_bucket_connectivity():
    # Send a request to the API server and store the response.
    # check s3 bucket connectivity for a static date
    response = requests.get('https://jobfeed-assignment-data.s3.eu-west-1.amazonaws.com/Jobs.2021-07-07.0.xml')

    # Confirm that the request-response cycle completed successfully.
    assert_true(response.ok)



if __name__ == "__main__":
    print("Running some basic tests")

    test_api_post_request_response()
    test_api_delete_request_response()
    test_s3_bucket_connectivity()

    print("All test cases passed successfully")

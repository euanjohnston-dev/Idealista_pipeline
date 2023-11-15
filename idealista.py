import json
from google.auth.transport.requests import Request
import dlt
from google.cloud import secretmanager_v1
from google.auth.transport.requests import Request


def access_secret_version(project_id, secret_id, version_id):
    client = secretmanager_v1.SecretManagerServiceClient()
    secret_name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    
    # Create an AccessSecretVersionRequest with the correct input
    request = secretmanager_v1.AccessSecretVersionRequest(name=secret_name)
    
    response = client.access_secret_version(request)
    return response.payload.data.decode('UTF-8')


@dlt.source
def property_analytics_source(api_secret_key=None):
    # Set the default value inside the function
    if api_secret_key is None:
        api_secret_key = json.loads(access_secret_version("propertyanalytics-404010", "keyfile", version_id="3"))
    return property_analytics_resource(api_secret_key)

def _create_auth_headers(api_secret_key=None):
    # Set the default value inside the function
    if api_secret_key is None:
        api_secret_key = json.loads(access_secret_version("propertyanalytics-404010", "keyfile", version_id="3"))

    credentials, _ = google.auth.default()
    auth_request = Request(credentials)
    credentials.refresh(auth_request)

    headers = {"Authorization": f"Bearer {credentials.token}"}
    return headers

@dlt.resource(write_disposition="append")
def property_analytics_resource(api_secret_key=None):
    if api_secret_key is None:
        api_secret_key = json.loads(access_secret_version("propertyanalytics-404010", "keyfile", version_id="3"))
    headers = _create_auth_headers(api_secret_key)

    # Check if authentication headers look fine
    print(headers)

    url = "https://idealista2.p.rapidapi.com/properties/list"

    # Use a different variable name to avoid overwriting the headers
    rapidapi_headers = {
        "X-RapidAPI-Key": "273f1c69a5mshe3d37237672b857p100581jsn241dc8ac149d",
        "X-RapidAPI-Host": "idealista2.p.rapidapi.com"
    }

    data = []
    page = 1
    
    # (make dynamic as currently isn't)
    while page <= 6:
        
        querystring = {
            "locationId": "0-EU-PT-08-03",
            "locationName": "Aljezur, Faro",
            "operation": "sale",
            "numPage": page,
            "maxItems": "40",
            "sort": "asc",
            "locale": "en",
            "country": "pt"
        }
        response = requests.get(url, headers={**headers, **rapidapi_headers}, params=querystring)
        response.raise_for_status()
        data.append(response.json())
        page += 1

    yield data

def idealista_run():
    # configure the pipeline with your destination details
    pipeline = dlt.pipeline(
        pipeline_name='idealista_list',
        destination='bigquery', 
        staging='filesystem', # add this to activate the staging location
        dataset_name='property_analytics'    
        )


    data = list(property_analytics_resource())

    # run the pipeline with your parameters
    load_info = pipeline.run(property_analytics_source())

    # pretty print the information on data that was loaded
    print(load_info)

import ibm_boto3
from ibm_botocore.client import Config

API_KEY = "INSERT YOUR API KEY HERE"
RESOURCE_INSTANCE_ID = "INSERT YOUR RESOURCE INSTANCE ID"
AUTH_ENDPOINT = "https://iam.cloud.ibm.com/identity/token"
ENDPOINT_URL = "https://s3.au-syd.cloud-object-storage.appdomain.cloud"

cos = ibm_boto3.client("s3",
    ibm_api_key_id=API_KEY,
    ibm_service_instance_id=RESOURCE_INSTANCE_ID,
    ibm_auth_endpoint=AUTH_ENDPOINT,
    config=Config(signature_version="oauth"),
    endpoint_url=ENDPOINT_URL
)

try:
    response = cos.list_buckets()
    print("✅ COS authentication successful.")
    for bucket in response["Buckets"]:
        print(f" - {bucket['Name']}")
except Exception as e:
    print("❌ COS authentication failed.")
    print("Error:", e)
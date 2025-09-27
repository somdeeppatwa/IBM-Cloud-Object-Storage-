import ibm_boto3
from ibm_botocore.client import Config

# === Credentials ===
API_KEY = "INSERT YOU API KEY "
RESOURCE_INSTANCE_ID = "INSERT YOUR RESOURCE INSTANCE ID"
AUTH_ENDPOINT = "https://iam.cloud.ibm.com/identity/token"
ENDPOINT_URL = "https://s3.au-syd.cloud-object-storage.appdomain.cloud"

# === Bucket Name ===
BUCKET_NAME = "cos-bucket-2025" 
# === Initialize COS client ===
cos = ibm_boto3.client("s3",
    ibm_api_key_id=API_KEY,
    ibm_service_instance_id=RESOURCE_INSTANCE_ID,
    ibm_auth_endpoint=AUTH_ENDPOINT,
    config=Config(signature_version="oauth"),
    endpoint_url=ENDPOINT_URL
)

# === Upload file function ===
def upload_file(file_name):
    try:
        cos.upload_file(Filename=file_name, Bucket=BUCKET_NAME, Key=file_name)
        print(f"✅ File uploaded: {file_name}")
    except Exception as e:
        print("❌ Upload failed:", e)

# === Upload example ===
upload_file("sample.txt")  # Make sure sample.txt exists in the same folder

import ibm_boto3
from ibm_botocore.client import Config
import time

# === Credentials & Config ===
API_KEY = "INSERT YOUR API KEY HERE"
RESOURCE_INSTANCE_ID = "INSERT YOUR RESOURCE ID HERE"
AUTH_ENDPOINT = "https://iam.cloud.ibm.com/identity/token"
ENDPOINT_URL = "https://s3.au-syd.cloud-object-storage.appdomain.cloud"

# === Initialize COS client ===
cos = ibm_boto3.client("s3",
    ibm_api_key_id=API_KEY,
    ibm_service_instance_id=RESOURCE_INSTANCE_ID,
    ibm_auth_endpoint=AUTH_ENDPOINT,
    config=Config(signature_version="oauth"),
    endpoint_url=ENDPOINT_URL
)

# === Create Bucket ===
def create_bucket(bucket_name):
    try:
        cos.create_bucket(Bucket=bucket_name)
        print(f"✅ Bucket created: {bucket_name}")
    except Exception as e:
        print("❌ Bucket creation failed:", e)

# === List Buckets ===
def list_buckets():
    try:
        response = cos.list_buckets()
        print("\n📦 Buckets:")
        for bucket in response["Buckets"]:
            print(f" - {bucket['Name']}")
    except Exception as e:
        print("❌ Listing buckets failed:", e)

# === Delete Bucket ===
def delete_bucket(bucket_name):
    try:
        # Must be empty before deletion
        objects = cos.list_objects_v2(Bucket=bucket_name)
        for obj in objects.get("Contents", []):
            cos.delete_object(Bucket=bucket_name, Key=obj["Key"])
        cos.delete_bucket(Bucket=bucket_name)
        print(f"🗑 Bucket deleted: {bucket_name}")
    except Exception as e:
        print("❌ Bucket deletion failed:", e)

# === Rename Bucket (Copy contents to new bucket, delete old) ===
def rename_bucket(old_name, new_name):
    try:
        create_bucket(new_name)
        objects = cos.list_objects_v2(Bucket=old_name)
        for obj in objects.get("Contents", []):
            copy_source = {'Bucket': old_name, 'Key': obj['Key']}
            cos.copy_object(Bucket=new_name, Key=obj['Key'], CopySource=copy_source)
        delete_bucket(old_name)
        print(f"✏ Bucket renamed: {old_name} → {new_name}")
    except Exception as e:
        print("❌ Bucket rename failed:", e)

# === Run Operations ===
timestamp = int(time.time())
bucket1 = f"(GIVE YOUR BUCKET NAME)-{timestamp}"
bucket2 = f"(GIVE YOUR BUCKET NAME)-{timestamp}"

create_bucket(bucket1)
list_buckets()
rename_bucket(bucket1, bucket2)
list_buckets()
delete_bucket(bucket2)
list_buckets()
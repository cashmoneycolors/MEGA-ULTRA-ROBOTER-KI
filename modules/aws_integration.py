"""AWS Integration - S3, EC2, Lambda Services"""
from core.key_check import require_keys
import os
from dotenv import load_dotenv

load_dotenv()

try:
    import boto3
    AWS_AVAILABLE = True
except ImportError:
    AWS_AVAILABLE = False
    print("⚠️ boto3 nicht installiert. Run: pip install boto3")

@require_keys
def run(*args):
    """Testet AWS Verbindung"""
    if not AWS_AVAILABLE:
        return {"status": "error", "message": "boto3 package fehlt"}

    access_key = os.getenv("AWS_ACCESS_KEY_ID")
    secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    region = os.getenv("AWS_REGION", "eu-central-1")

    if not access_key or not secret_key:
        return {"status": "error", "message": "AWS Keys nicht konfiguriert"}

    try:
        # Test S3 Verbindung
        s3 = boto3.client(
            's3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region
        )

        buckets = s3.list_buckets()

        return {
            "status": "success",
            "message": "AWS verbunden",
            "region": region,
            "buckets_count": len(buckets['Buckets']),
            "services": ["S3", "EC2", "Lambda"]
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def upload_to_s3(file_path, bucket_name, object_name=None):
    """Lädt Datei zu S3 hoch"""
    if not AWS_AVAILABLE:
        raise RuntimeError("boto3 nicht installiert")

    access_key = os.getenv("AWS_ACCESS_KEY_ID")
    secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    region = os.getenv("AWS_REGION", "eu-central-1")

    if not object_name:
        object_name = os.path.basename(file_path)

    try:
        s3 = boto3.client(
            's3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region
        )

        s3.upload_file(file_path, bucket_name, object_name)

        url = f"https://{bucket_name}.s3.{region}.amazonaws.com/{object_name}"

        return {
            "status": "success",
            "bucket": bucket_name,
            "object": object_name,
            "url": url
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def download_from_s3(bucket_name, object_name, local_path):
    """Lädt Datei von S3 herunter"""
    if not AWS_AVAILABLE:
        raise RuntimeError("boto3 nicht installiert")

    access_key = os.getenv("AWS_ACCESS_KEY_ID")
    secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    region = os.getenv("AWS_REGION", "eu-central-1")

    try:
        s3 = boto3.client(
            's3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region
        )

        s3.download_file(bucket_name, object_name, local_path)

        return {
            "status": "success",
            "bucket": bucket_name,
            "object": object_name,
            "local_path": local_path
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def list_s3_objects(bucket_name, prefix=""):
    """Listet S3 Objekte auf"""
    if not AWS_AVAILABLE:
        raise RuntimeError("boto3 nicht installiert")

    access_key = os.getenv("AWS_ACCESS_KEY_ID")
    secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    region = os.getenv("AWS_REGION", "eu-central-1")

    try:
        s3 = boto3.client(
            's3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region
        )

        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

        objects = []
        if 'Contents' in response:
            objects = [
                {"key": obj['Key'], "size": obj['Size'], "modified": str(obj['LastModified'])}
                for obj in response['Contents']
            ]

        return {
            "status": "success",
            "bucket": bucket_name,
            "objects": objects,
            "count": len(objects)
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_ec2_instances():
    """Listet EC2 Instanzen auf"""
    if not AWS_AVAILABLE:
        raise RuntimeError("boto3 nicht installiert")

    access_key = os.getenv("AWS_ACCESS_KEY_ID")
    secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    region = os.getenv("AWS_REGION", "eu-central-1")

    try:
        ec2 = boto3.client(
            'ec2',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region
        )

        response = ec2.describe_instances()

        instances = []
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instances.append({
                    "id": instance['InstanceId'],
                    "type": instance['InstanceType'],
                    "state": instance['State']['Name'],
                    "launch_time": str(instance['LaunchTime'])
                })

        return {
            "status": "success",
            "instances": instances,
            "count": len(instances)
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def install():
    """Installiert boto3"""
    import subprocess
    print("📦 Installiere boto3...")
    subprocess.run(["pip", "install", "-U", "boto3"], check=True)
    return {"status": "success", "message": "boto3 installiert"}

def describe():
    return "AWS Integration - S3 Storage, EC2 Instances, Lambda Functions"

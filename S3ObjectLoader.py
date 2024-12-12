import boto3
from botocore.exceptions import NoCredentialsError
import glob
import os

def upload_file_to_s3(file_path, bucket_name, object_name=None, region='us-east-1', aws_access_key_id=None, aws_secret_access_key=None):
    """
    Upload a file to an S3 bucket.

    :param file_path: Path to the file to be uploaded
    :param bucket_name: Name of the bucket where the file will be uploaded
    :param object_name: S3 object name (key) under which the file will be stored
    :param region: AWS region where the bucket is located (default is 'us-east-1')
    :param aws_access_key_id: AWS access key ID
    :param aws_secret_access_key: AWS secret access key
    :return: True if the file was uploaded successfully, False otherwise
    """
    try:
        # Create an S3 client with explicit access key and secret key
        s3 = boto3.client('s3', region_name=region, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

        # If S3 object_name was not specified, use the file name
        if object_name is None:
            object_name = file_path

        # Upload the file
        s3.upload_file(file_path, bucket_name, object_name)

        print(f"File '{file_path}' uploaded to '{bucket_name}' as '{object_name}'.")
        return True

    except NoCredentialsError:
        print("Credentials not available.")
        return False

    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def upload_files_in_directory(directory_path, bucket_name, aws_access_key_id=None, aws_secret_access_key=None):
    """
    Upload all files in a directory to an S3 bucket.

    :param directory_path: Path to the directory containing files to be uploaded
    :param bucket_name: Name of the bucket where the files will be uploaded
    :param aws_access_key_id: AWS access key ID
    :param aws_secret_access_key: AWS secret access key
    """
    # Use glob to get a list of all files in the directory
    files_to_upload = glob.glob(os.path.join(directory_path, '*'))

    # Iterate through the list of files and upload each to S3
    for file_path in files_to_upload:
        upload_file_to_s3(file_path, bucket_name, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)


# Replace 'your-unique-bucket-name' with your S3 bucket name
bucket_name = 'musicstorage-3144'

# Replace 'your-access-key-id' and 'your-secret-access-key' with your AWS access key and secret key
access_key_id = 'your-access-key-id'
secret_access_key = 'your-secret-access-key'

directories = [dir for dir in glob.glob(os.path.join("Data/images_original/", '*')) if os.path.isdir(dir)]
print(directories)
# Upload the file to the S3 bucket with explicit credentials
for dir in directories:
    upload_files_in_directory(dir, bucket_name, aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)


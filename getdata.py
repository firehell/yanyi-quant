import boto3
from botocore.config import Config
import gzip
import os
import datetime

# Initialize a session using your credentials
session = boto3.Session(
   aws_access_key_id='1c8e3e1a-7f13-4a88-a436-62a01886e16f',
   aws_secret_access_key='_tpwPsCcsASx5DcrD1NpUEA1NHxqr5gt',
)

# Create a client with your session and specify the endpoint
s3 = session.client(
   's3',
   endpoint_url='https://files.polygon.io',
   config=Config(signature_version='s3v4'),
)

# Specify the bucket name
bucket_name = 'flatfiles'

# Specify the base prefix for the data
# base_prefix = 'us_stocks_sip/minute_aggs_v1/2024/12/'
base_prefix = 'us_stocks_sip/minute_aggs_v1/'

prefix = 'us_stocks_sip' 
paginator = s3.get_paginator('list_objects_v2')

# # List of dates for the files you want to process

target_date = datetime.date(2020, 3, 24)
dates_to_process = []
for page in paginator.paginate(Bucket='flatfiles', Prefix=prefix):
    for obj in page['Contents']:
        if 'minute_aggs_v1' not in obj['Key']:
            parts = obj['Key'].split('/')
            # 提取年月日信息
            year_str = parts[-3]
            month_str = parts[-2]
            date_str = parts[-1].split('.')[0].split('-')[-1]  # 获取日期部分

            try:
                year = int(year_str)
                month = int(month_str)
                day = int(date_str)
                current_date = datetime.date(year, month, day)

                if current_date >= target_date:
                    result = '/'.join(parts[-3:])
                    dates_to_process.append(obj['Key'])
                    print(obj['Key'])
            except ValueError:
                print(f"Could not parse date from key: {obj['Key']}")


# # Specify the local directory to save the downloaded files
local_download_directory = './downloaded_files/'
os.makedirs(local_download_directory, exist_ok=True)

for date_str in dates_to_process:
    # Construct the S3 object key name for the current date
    object_key = date_str
    print('object_key: ' + object_key)
    
    # This splits the object_key string by '/' and takes the last segment as the file name
    compressed_file_name = object_key.split('/')[-1]

    # This constructs the full local file path for the compressed file
    compressed_file_path = os.path.join(local_download_directory, compressed_file_name)

    try:
        # Download the file
        s3.download_file(bucket_name, object_key, compressed_file_path)
        print(f"Successfully downloaded: {compressed_file_path}")

        # --- 解压 .gz 文件并删除原始文件 ---
        decompressed_file_name = compressed_file_name[:-3]  # Remove the '.gz' extension
        decompressed_file_path = os.path.join(local_download_directory, decompressed_file_name)

        try:
            with gzip.open(compressed_file_path, 'rb') as f_in:
                with open(decompressed_file_path, 'wb') as f_out:
                    f_out.write(f_in.read())
            print(f"Successfully decompressed to: {decompressed_file_path}")

            # Delete the original .gz file
            os.remove(compressed_file_path)
            print(f"Successfully deleted the original compressed file: {compressed_file_path}")

        except FileNotFoundError:
            print(f"Error: Compressed file not found at: {compressed_file_path}")
        except Exception as e:
            print(f"An error occurred during decompression for {compressed_file_name}: {e}")

    except Exception as e:
        print(f"Error downloading {object_key}: {e}")

print("Finished processing all files.")
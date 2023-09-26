import json
import os
import zipfile
from pathlib import Path

import boto3


def zip_directory(directory_path, zip_path):
    # Creating a Zip file containing everything in the directory_path
    with zipfile.ZipFile(zip_path, "w") as zip:
        for folderName, subfolders, filenames in os.walk(directory_path):
            for filename in filenames:
                # Create complete filepath of file in directory
                filePath = os.path.join(folderName, filename)
                # Add file to zip
                zip.write(filePath, arcname=os.path.relpath(filePath, directory_path))


def get_zip_info(zip_path):
    # Printing information of what it zipped
    with zipfile.ZipFile(zip_path, "r") as zip:
        zip.printdir()


def upload_to_s3(zip_path, bucket_name):
    # Upload zip to S3
    s3 = boto3.client("s3")
    s3.upload_file(zip_path, bucket_name, f"extras/{Path(zip_path).name}")


def print_import_instruction(bucket_name, zip_path):
    # Print in pretty format exactly how to import this inside your glue job scripts
    instructions = {
        "DefaultArguments": {"--extra-py-files": f"s3://{bucket_name}/extras/{Path(zip_path).name}"},
        "PythonImportStatement": "from assets.extras import hello_world",
        "FunctionCall": "hello_world.hello_world()",
    }
    print(json.dumps(instructions, indent=4))


def zip_glue_dependencies(bucket_name):
    directory_path = os.path.join(os.path.dirname(__file__), "assets", "extras")
    zip_path = os.path.join(os.path.dirname(__file__), "assets", "extras.zip")

    zip_directory(directory_path, zip_path)
    get_zip_info(zip_path)
    # COMMENTED OUT because we are using bucketDeployment instead
    # upload_to_s3(zip_path, bucket_name)
    print_import_instruction(bucket_name, zip_path)


### USAGE ###
# Import like so:

# # Add the parent directory to the system path
# sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

# # Now import the zip_util module
# import zip_util

# CAll like so:

# bucket_name = "jochem-glue-job-extra-param-test-bucket"

# bucket = aws_s3.Bucket(self, bucket_name, bucket_name=bucket_name)

# zip_util.zip_glue_dependencies(bucket.bucket_name)

# aws_s3_deployment.BucketDeployment(
#     self, "deployment", sources=[aws_s3_deployment.Source.asset("./assets/")], destination_bucket=bucket
# )

#
#

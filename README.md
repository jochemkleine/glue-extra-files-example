# Glue Extra Python Files

A quick sample for how to add and import "extra files" (i.e. other classes, utilities) to Glue jobs. Some values are hardcoded

## Overview

This repository provides a systematic way to handle extra dependencies for AWS Glue Jobs, allowing users to bundle additional Python files and modules into a zip file, which is then uploaded to an Amazon S3 bucket. These extra files can contain utility functions, custom libraries, or any other code that your Glue job requires to run.

## Preparing Your Dependencies

1. **Creating the Extras Directory:**  
   Create a directory named `assets` at the root level of your project. Inside the `assets` directory, create another directory named `extras`. This is where you will place all the extra files and modules that your Glue job will need.
   
    ```plaintext
    project-root-directory/
    └── assets/
        └── extras/
    ```

2. **Adding Your Files:**  
   Place your extra files and modules inside the `extras` directory. This could include utility files like a log helper, a DynamoDB service module, a custom data processing library, or any other Python scripts your Glue job needs.

## Configuring Your CDK Stack

The `ExtraFileGlueJobTestStack` class in your CDK stack script handles the orchestration of zipping up your extra dependencies, uploading them to S3, and configuring your Glue job to use these extras. Here's an outline of how it's structured:

1. **Role Creation:**  
   A role for the Glue job is created with necessary permissions.

2. **Bucket Creation:**  
   An S3 bucket is created to hold your Glue job script and extra dependencies.

3. **Zipping Extras:**  
   The `zip_glue_dependencies` function is called to zip up everything in the `assets/extras` directory.

4. **Uploading to S3:**  
   The zipped extras and your Glue job script are uploaded to the S3 bucket using the `BucketDeployment` construct.

5. **Glue Job Creation:**  
   A Glue job is created with the necessary configurations to use the zipped extras from S3.

```python
class ExtraFileGlueJobTestStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # ... (rest of your code)

        # Ensure the zip_util module is importable
        sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
        import zip_util

        # Zip the extras and get import instructions
        zip_util.zip_glue_dependencies(bucket_name=bucket_name)

        # ... (rest of your code)

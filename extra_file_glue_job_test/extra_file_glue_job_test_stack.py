import os
import subprocess
import sys

from aws_cdk import Stack  # Duration,; aws_sqs as sqs,
from aws_cdk import aws_s3  # Duration,; aws_sqs as sqs,
from aws_cdk import aws_glue as glue
from aws_cdk import aws_iam as iam
from aws_cdk import aws_s3_deployment
from constructs import Construct

# Add the parent directory to the system path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

# Now import the zip_util module
import zip_util


class ExtraFileGlueJobTestStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        glue_job_role = iam.Role(
            self,
            "GlueJobRole",
            assumed_by=iam.ServicePrincipal("glue.amazonaws.com"),
            managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSGlueServiceRole")],
        )

        bucket_name = "jochem-glue-job-extra-param-test-bucket"

        bucket = aws_s3.Bucket(self, bucket_name, bucket_name=bucket_name)

        zip_util.zip_glue_dependencies(bucket_name=bucket_name)

        aws_s3_deployment.BucketDeployment(
            self, "deployment", sources=[aws_s3_deployment.Source.asset("./assets/")], destination_bucket=bucket
        )

        job = glue.CfnJob(
            self,
            "glue_job",
            name="glue_job",
            command=glue.CfnJob.JobCommandProperty(
                name="glueetl",
                python_version="3",
                script_location=f"s3://{bucket.bucket_name}/glue_job.py",
            ),
            role=glue_job_role.role_arn,
            glue_version="4.0",
            default_arguments={"--extra-py-files": f"s3://{bucket.bucket_name}/extras/extras.zip"},
            timeout=3,
        )

        bucket.grant_read_write(glue_job_role)

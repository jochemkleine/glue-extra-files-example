import aws_cdk as core
import aws_cdk.assertions as assertions

from extra_file_glue_job_test.extra_file_glue_job_test_stack import ExtraFileGlueJobTestStack

# example tests. To run these tests, uncomment this file along with the example
# resource in extra_file_glue_job_test/extra_file_glue_job_test_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = ExtraFileGlueJobTestStack(app, "extra-file-glue-job-test")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })

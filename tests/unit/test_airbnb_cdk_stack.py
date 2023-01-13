import aws_cdk as core
import aws_cdk.assertions as assertions

from airbnb_cdk.airbnb_cdk_stack import AirbnbCdkStack

# example tests. To run these tests, uncomment this file along with the example
# resource in airbnb_cdk/airbnb_cdk_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = AirbnbCdkStack(app, "airbnb-cdk")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })

import os
import sys

from aws_cdk.core import App

"""
Import main stack.
"""

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_PATH)
from b_twilio_sdk_layer_test.integration.infrastructure import Infrastructure

"""
Create CDK app.
"""

app = App()
Infrastructure(app)
app.synth()

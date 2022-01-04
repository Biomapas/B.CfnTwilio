import os
import sys

from aws_cdk.core import App

"""
Import main stack.
"""
from b_cfn_twilio_test.integration.infrastructure import Infrastructure

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_PATH)

"""
Create CDK app.
"""

app = App()
Infrastructure(app)
app.synth()

import os
from pathlib import Path

import sagemaker
from sagemaker.workflow.pipeline_context import LocalPipelineSession, PipelineSession

class Configuration:
    def __init__(self, local_mode=True):
        self.local_mode = local_mode

        self.bucket = os.environ["BUCKET"]
        self.role = os.environ["ROLE"]

        self.comet_api_key = os.environ.get("COMET_API_KEY", None)
        self.comet_project_name = os.environ.get("COMET_PROJECT_NAME", None)

        architecture = os.uname().machine
        self.is_arm64_architecture = architecture == "arm64"

        self.pipeline_session = (
            PipelineSession(default_bucket=self.bucket)
            if not self.local_mode
            else None
        )

        self.config = self.load()

    def load(self):
        if self.local_mode:
            return {
                "session": LocalPipelineSession(default_bucket=self.bucket),
                "instance_type": "local",
                "image": (
                    "sagemaker-tensorflow-toolkit-local" if self.is_arm64_architecture else None
                ),
                "framework_version": "2.12",
                "py_version": "py310"
            }
        else:
            return {
                "session": self.pipeline_session,
                "instance_type": "ml.m5.xlarge",
                "image": None,
                "framework_version": "2.12",
                "py_version": "py310"
            }
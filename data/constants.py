import os

JENKINS_URL      = os.environ.get("JENKINS_URL")
NIGHTLY_PIPELINE = os.environ.get('nightly_pipeline')

USER_NAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")

REPORTS_PATH = "/mnt/nightly_reports"

AZURE_OPENAI_URL = os.getenv("AZURE_OPENAI_URL")
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")

OPENAI_API_VERSION = "2024-08-01-preview"
OPENAI_MODEL = "gpt-4o-mini"



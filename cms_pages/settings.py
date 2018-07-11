# -*- coding: utf-8 -*-
import os

CMS_URL = os.environ["CMS_URL"]
CMS_SIGNATURE_SECRET_API_KEY = os.environ["CMS_SIGNATURE_SECRET_API_KEY"]
CMS_API_PAGES_ENDPOINT = os.getenv("CMS_API_PAGES_ENDPOINT", "api/pages/")

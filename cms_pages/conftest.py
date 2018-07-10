# -*- coding: utf-8 -*-
import pytest
from directory_api_client.testapiclient import DirectoryTestAPIClient

from cms_pages import settings
from cms_pages.settings import CMS_SIGNATURE_SECRET_API_KEY


@pytest.fixture
def cms_client():
    base_url = settings.CMS_URL
    return DirectoryTestAPIClient(
        base_url=base_url, api_key=CMS_SIGNATURE_SECRET_API_KEY
    )

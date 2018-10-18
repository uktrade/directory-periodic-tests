# -*- coding: utf-8 -*-
from django.conf import settings

from cms_pages.settings import (
    DIRECTORY_CMS_API_CLIENT_API_KEY,
    DIRECTORY_CMS_API_CLIENT_BASE_URL,
)


settings.configure(
    DIRECTORY_CMS_API_CLIENT_BASE_URL=DIRECTORY_CMS_API_CLIENT_BASE_URL,
    DIRECTORY_CMS_API_CLIENT_API_KEY=DIRECTORY_CMS_API_CLIENT_API_KEY,
    DIRECTORY_CMS_API_CLIENT_SENDER_ID="tests",
    DIRECTORY_CMS_API_CLIENT_SERVICE_NAME="directory",
    DIRECTORY_CMS_API_CLIENT_DEFAULT_TIMEOUT=55,
    DIRECTORY_CMS_API_CLIENT_CACHE_EXPIRE_SECONDS=2592000,
    CACHES={
        "cms_fallback": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "unique-snowflake",
        }
    },
)

# -*- coding: utf-8 -*-
from cms_pages.settings import CMS_API_PAGES_ENDPOINT


def get_page_ids_by_type(cms_client, page_type):
    page_ids = []

    # get first page of results
    url = "{}?type={}".format(CMS_API_PAGES_ENDPOINT, page_type)
    response = cms_client.get(url)
    assert response.status_code == 200

    # get IDs of all pages from the response
    content = response.json()
    page_ids += [page["id"] for page in content["items"]]

    total_count = content["meta"]["total_count"]
    while len(page_ids) < total_count:
        offset = len(content["items"])
        url = "{}?type={}&offset={}".format(
            CMS_API_PAGES_ENDPOINT, page_type, offset
        )
        response = cms_client.get(url)
        assert response.status_code == 200
        content = response.json()
        page_ids += [page["id"] for page in content["items"]]

    assert len(list(sorted(page_ids))) == total_count
    return page_ids

import json
import os

import allure
from allure_commons.types import AttachmentType
from curlify import to_curl
from requests import sessions


resources_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../resources'))


def base_url(url):
    return str(url)


def api(base_url, method, url, **kwargs):
    new_url = base_url + url
    method = method.upper()
    with allure.step(f"{method} {url}"):
        with sessions.Session() as session:
            response = session.request(method=method, url=new_url, **kwargs)
            message = to_curl(response.request)
            if response.content:
                allure.attach(body=json.dumps(response.json(), indent=4).encode("utf8"), name="Response Json",
                              attachment_type=AttachmentType.JSON, extension='json')
                allure.attach(body=message.encode("utf8"), name="Curl", attachment_type=AttachmentType.TEXT,
                              extension='txt')
            else:
                allure.attach(body=message.encode("utf8"), name="Curl", attachment_type=AttachmentType.TEXT,
                              extension='txt')
    return response

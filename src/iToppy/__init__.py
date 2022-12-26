"""
Python itop Module

.. include:: ../../README.md
"""
import json
import requests
from enum import Enum
from typing import List, Union
from base64 import b64encode
from . import models as IM

class iTop:
    """
    Stores connection and session information for the iTop Rest API
    """
    def __init__(
        self, 
        url: str,
        username: str, 
        password: str,
        version: str = "1.3",
        auth: IM.iAuth = IM.iAuth.FORM,
        verify: bool = True,
        timeout: int = 10
    ):
        
        if "webservices/rest.php" not in url:
            if url[-1:] != "/":
                url += "/"
            url += "webservices/rest.php?version=" + version
 
        self.session = requests.session()
        self.headers = {}
        self.body = {}
                
        if auth == IM.iAuth.FORM:
            self.body = {
                "auth_user": username,
                "auth_pwd": password
                
            }
        
        elif auth == IM.iAuth.BASIC:
            self.headers = {
                "Authorization": f"Basic {b64encode(f'{username}:{password}'.encode('utf-8')).decode('utf-8')}"
            }

        self.req_opts = {
            "url": url,
            "verify": verify,
            "timeout": timeout,
            "headers": self.headers if len(self.headers) > 0 else None
        }

    def make_request(self, json_data: str) -> dict:
        resp = self.session.post(
            **self.req_opts,
            data={**self.body, "json_data": json_data}
        )
        
        if resp.status_code != 200:
            raise Exception(f"iTop API returned status code {resp.status_code}: {resp.text}")
        
        response = resp.json()
        
        if response['code'] != 0:
            err = IM.iError(response['code'])
            raise Exception(f"iTop API returned error code {response['code']} ({err}): {response['message']}")

        return response

    def get_oql(self, itop_class: str, key: Union[dict, IM.iOQLBuilder]) -> str:
        if isinstance(key, IM.iOQLBuilder):
            return str(key)

        wheres = ' AND '.join([IM.iOQLBuilder.get_where(k, '"', v) for k, v in key.items()])

        return f"SELECT {itop_class}{' WHERE '+wheres if len(wheres) > 0 else ''}"

    def list_operations(self) -> List[IM.iOperation]:
        return [
            IM.iOperation(**x) for x in self.make_request(
                json.dumps({"operation": "list_operations"})
            )["operations"]
        ]

    def test_connection(self) -> bool:
        return self.list_operations > 0 
    
    def get(
        self, 
        itop_class: str, 
        key: Union[str, dict, IM.iOQLBuilder] = None, 
        fields: Union[list, set, tuple, str] = None,
        limit: int = None,
        page: int = None
    ) -> IM.iResponse:
        json_data = {
            "operation": "core/get",
            "class": itop_class,
            "output_fields": ', '.join(fields) if fields is not None else "*",
            "key": f"SELECT {itop_class}"
        }

        if key is not None:
            json_data['key'] = key if isinstance(key, str) else self.get_oql(itop_class, key),

        if limit is not None:
            json_data['limit'] = limit
        
        if page is not None:
            json_data['page'] = page

        return IM.iResponse.from_response(self.make_request(json.dumps(json_data)))

    def create(self, itop_class: str, fields: dict) -> IM.iResponse:
        pass
    
    def update(self, itop_class: str, fields: dict) -> IM.iResponse:
        pass
    
    def apply_stimulus(self, itop_class: str, key: str, stimulus: str) -> IM.iResponse:
        pass
    
    
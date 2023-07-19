#!/usr/bin/env python3

import __constants__ as vc
import os
import requests
import json

import mausy5043_common.funfile as mf

DEBUG = False
HERE = os.path.realpath(__file__).split("/")
MYID = HERE[-1]


class VolvoAPI:
    """Super class to hold functions"""

    def __init__(self, debug=False):
        self.debug = debug
        self.api_primary_key = vc.API_KEY[0]
        self.api_secondary_key = vc.API_KEY[1]
        self.api_tokens = vc.API_TOKEN
        self.api_token = None
        self.vin = vc.API_VIN
        self.call_urls = []
        self.base_url = ""

    def get(self, accept="application/json"):
        _accept = accept
        _headers = {
            "Content-type": "application/json",
            "Accept": f"{_accept}",
            "authorization": f"Bearer {self.api_token}",
            "vcc-api-key": self.api_primary_key,
        }
        for _url in self.call_urls:
            mf.syslog_trace(_url, False, self.debug)
            _response = requests.get(_url, headers=_headers, timeout=10)
            #     mf.syslog_trace(f"Response Status Code: {response.status_code}", False, self.debug)
            #     for key in response.headers:
            #         mf.syslog_trace(f"   {key} :: {response.headers[key]}", False, self.debug)
            #     mf.syslog_trace("***** ***** *****\n", False, self.debug)

            _result = json.loads(_response.content)
            if self.debug:
                mf.syslog_trace(f"Result data: ", False, self.debug)
                for _key in _result:
                    if _key == "data":
                        for _data_key in _result[_key]:
                            mf.syslog_trace(
                                f"      {_data_key} :: {_result[_key][_data_key]}",
                                False,
                                self.debug,
                            )
                    else:
                        mf.syslog_trace(f"   {_key} :: {_result[_key]}", False, self.debug)

            # TODO: The specification "knows" what responses are to be expected
            #       for each path. Use that here to our advantage.
            if _response.status_code == 400:
                mf.syslog_trace(
                    "Bad Request - Request contains an unaccepted input", False, self.debug
                )
            if _response.status_code == 401:
                mf.syslog_trace("Unauthorized or TOKEN expired", False, self.debug)
            if _response.status_code == 403:
                mf.syslog_trace("Resource forbidden", False, self.debug)
            if _response.status_code == 404:
                mf.syslog_trace("Not found", False, self.debug)
            if _response.status_code == 500:
                mf.syslog_trace("Internal Server Error", False, self.debug)

        return _result

#!/usr/bin/env python3

import __constants__ as vc
import os
import requests
import json

import mausy5043_common.funfile as mf

DEBUG = False
HERE = os.path.realpath(__file__).split("/")
MYID = HERE[-1]


class VolvoAPI():
    """Super class to hold functions"""
    def __init__(self, debug=False):
        self.debug = debug
        self.api_primary_key = vc.API_KEY[0]
        self.api_secondary_key = vc.API_KEY[1]
        self.api_token = vc.API_TOKEN
        self.vin = vc.API_VIN
        self.call_urls = []
        self.base_url = ""

    def get(self):
        accept = "application/json"
        headers = {
            "Content-type": "application/json",
            "Accept": f"{accept}",
            "authorization": f"Bearer {self.api_token}",
            "vcc-api-key": self.api_primary_key,
        }
        for url in self.call_urls:
            response = requests.get(url, headers=headers, timeout=10)
            print(url, self.debug)
            if self.debug:
                mf.syslog_trace(f"Response Status Code: {response.status_code}", False, self.debug)
                for key in response.headers:
                    mf.syslog_trace(f"   {key} :: {response.headers[key]}", False, self.debug)
                mf.syslog_trace("***** ***** *****\n", False, self.debug)

            result = json.loads(response.content)
            if self.debug:
                mf.syslog_trace(f"Result data: ", False,self.debug)
                for key in result:
                    if key == "data":
                        for data_key in result[key]:
                            mf.syslog_trace(
                                f"      {data_key} :: {result[key][data_key]}", False,self.debug
                            )
                    else:
                        mf.syslog_trace(f"   {key} :: {result[key]}", False,self.debug)

            if response.status_code == 400:
                raise Exception("Bad Request - Request contains an unaccepted input")
            if response.status_code == 401:
                raise Exception("Unauthorized or TOKEN expired")
            if response.status_code == 403:
                raise Exception("Resource forbidden")
            if response.status_code == 404:
                raise Exception("Not found")
            if response.status_code == 500:
                raise Exception("Internal Server Error")

        return result

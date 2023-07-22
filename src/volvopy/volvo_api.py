#!/usr/bin/env python3
import random

import __constants__ as vc
import os
import requests
import json

import mausy5043_common.funfile as mf

DEBUG = False
HERE = os.path.realpath(__file__).split("/")
MYID = HERE[-1]


class VolvoAPI:
    """Base Class to connect and interact with the Volvo Energy API.

    ref.: https://developer.volvocars.com/apis/
    """

    def __init__(self, debug=False):
        self.debug = debug
        self.api_key = vc.API_KEY[round(random.random())]   # Select one of the keys for use
        # For testing a DEMO token is needed, which will be valid for 1 hr and can be generated
        # at one of the API websites (see the appropriate module for a link)
        self.api_token = None   # This holds the token
        self.vin = vc.API_VIN   # The VIN number of the car

        self.get_urls = []
        self.post_urls = []
        self.api = ""
        self.api_spec = {}
        self.base_url = ""

    def get_all(self, accept="application/json"):
        """GET all paths"""
        result = []
        vin = self.vin
        for path in self.api_spec["paths"]:
            try:
                if self.api_spec["paths"][path]["get"]:
                    # get the 'Accept' entry from the specification
                    accept = list(self.api_spec["paths"][path]["get"]["responses"]["200"]["content"])[0]# construct the headers
                    headers = {
                                "Content-type": "application/json",
                                "Accept": f"{accept}",
                                "authorization": f"Bearer {self.api_token}",
                                "vcc-api-key": self.api_key,
                                }
                    # construct the URL
                    try:
                        url = eval(f"f'{self.base_url}{path}'")

                        mf.syslog_trace(f"---\nGETting {url} ...", False, self.debug)
                        response = requests.get(url, headers=headers, timeout=10)
                        content = json.loads(response.content)

                        if self.debug:
                            mf.syslog_trace(f"Result data: ", False, self.debug)
                            for _key in content:
                                if _key == "data" and isinstance(content[_key], dict):
                                    for _data_key in content[_key]:
                                        mf.syslog_trace(
                                            f"      {_data_key} :: {content[_key][_data_key]}",
                                            False,
                                            self.debug,
                                        )
                                else:
                                    mf.syslog_trace(f"   {_key} :: {content[_key]}", False, self.debug)
                        result.append(content)
                    except:
                        pass
            except KeyError:
                mf.syslog_trace("", False, self.debug)
                mf.syslog_trace(f"** Skipping {path} ...", False, self.debug)

            # try:
            #     if self.api_spec["paths"][path]["post"]:
            #         pass
            # except KeyError:
            #     mf.syslog_trace(f"Skipping POST {path} ...", False, self.debug)



            # TODO: The specification "knows" what responses are to be expected
            #       for each path. Use that here to our advantage.
            # if _response.status_code == 400:
            #     mf.syslog_trace(
            #         "Bad Request - Request contains an unaccepted input", False, self.debug
            #     )
            # if _response.status_code == 401:
            #     mf.syslog_trace("Unauthorized or TOKEN expired", False, self.debug)
            # if _response.status_code == 403:
            #     mf.syslog_trace("Resource forbidden", False, self.debug)
            # if _response.status_code == 404:
            #     mf.syslog_trace("Not found", False, self.debug)
            # if _response.status_code == 500:
            #     mf.syslog_trace("Internal Server Error", False, self.debug)

        return result

#!/usr/bin/env python3

import __constants__ as vc
import os
import syslog

import mausy5043_common.funfile as mf
DEBUG = False
HERE = os.path.realpath(__file__).split("/")
# runlist id :
MYID = HERE[-1]


class Energy():
    """Class to connect and interact with the Volvo Energy API.

    ref.: https://developer.volvocars.com/apis/energy/v1/specification/
    """
    def __init__(self):
        self.api_primary_key = vc.API_KEY[0]
        self.api_secondary_key = vc.API_KEY[1]
        self.api_token = vc.API_TOKEN
        self.vin = vc.API_VIN
        vin = self.vin  # noqa
        api = 'energy'
        self.base_url = f"{vc.API_SPECIFICATIONS[api]['servers'][0]['url']}"
        self.call_urls = []
        for path in vc.API_SPECIFICATIONS[api]['paths']:
            url_path = eval(f"f'{path}'")
            self.call_urls.append(f"{self.base_url}{url_path}")
        print(f"Number of URLs: {len(self.call_urls)}")
        for item in self.call_urls:
            mf.syslog_trace(f"{item}", False, DEBUG)

if __name__ == "__main__":
    DEBUG = True
    a = Energy()

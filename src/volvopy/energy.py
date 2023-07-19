#!/usr/bin/env python3

import __constants__ as vc
from volvo_api import VolvoAPI
import os

import mausy5043_common.funfile as mf

DEBUG = False
HERE = os.path.realpath(__file__).split("/")
MYID = HERE[-1]


class Energy(VolvoAPI):
    """Class to connect and interact with the Volvo Energy API.

    ref.: https://developer.volvocars.com/apis/energy/v1/specification/
    """

    def __init__(self, debug=False):
        super().__init__(debug=debug)

        api = "energy"
        self.base_url = f"{vc.API_SPECIFICATIONS[api]['servers'][0]['url']}"
        vin = self.vin  # noqa
        for path in vc.API_SPECIFICATIONS[api]["paths"]:
            url_path = eval(f"f'{path}'")
            self.call_urls.append(f"{self.base_url}{url_path}")

        print(f"Number of URLs: {len(self.call_urls)}")
        for item in self.call_urls:
            mf.syslog_trace(f"{item}", False, self.debug)
        if self.api_tokens[api]:
            self.api_token = self.api_tokens[api]


if __name__ == "__main__":
    DEBUG = True
    a = Energy(debug=DEBUG)
    a.get(accept="application/vnd.volvocars.api.energy.vehicledata.v1+json")

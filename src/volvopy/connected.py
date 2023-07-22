#!/usr/bin/env python3

import __constants__ as vc
from volvo_api import VolvoAPI
import os

import mausy5043_common.funfile as mf

DEBUG = False
HERE = os.path.realpath(__file__).split("/")
MYID = HERE[-1]


class Connected_Vehicle(VolvoAPI):
    """Class to connect and interact with the Volvo Connected Vehicle API.

    ref.: https://developer.volvocars.com/apis/connected-vehicle/v1/specification/
    """

    def __init__(self, debug=False):
        super().__init__(debug=debug)

        self.api = "connected"
        self.api_token = vc.API_TOKEN[self.api]
        self.api_spec = vc.API_SPECIFICATIONS[self.api]
        self.base_url = f"{self.api_spec['servers'][0]['url']}"


if __name__ == "__main__":
    DEBUG = True
    a = Connected_Vehicle(debug=DEBUG)
    a.get_all(accept="application/vnd.volvocars.api.connected-vehicle.vehicledata.v1+json")

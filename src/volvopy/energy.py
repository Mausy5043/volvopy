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

        self.api = "energy"  # Name of the API.
        self.api_token = vc.API_TOKEN[self.api]
        self.api_spec = vc.API_SPECIFICATIONS[self.api]
        self.base_url = f"{self.api_spec['servers'][0]['url']}"


if __name__ == "__main__":
    DEBUG = True
    a = Energy(debug=DEBUG)
    a.get_all(accept="application/vnd.volvocars.api.energy.vehicledata.v1+json")

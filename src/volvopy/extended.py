#!/usr/bin/env python3

import os
import uuid

import mausy5043_common.funfile as mf

import __constants__ as vc
from volvo_api import VolvoAPI

DEBUG = False
HERE = os.path.realpath(__file__).split("/")
MYID = HERE[-1]


class Extended_Vehicle(VolvoAPI):
    """Class to connect and interact with the Volvo Extended Vehicle API.

    ref.:https://developer.volvocars.com/apis/extended-vehicle/v1/specification/
    """

    def __init__(self, debug=False):
        super().__init__(debug=debug)

        self.api = "extended"
        self.api_token = vc.API_TOKEN[self.api]
        self.api_spec = vc.API_SPECIFICATIONS[self.api]
        self.guid = str(uuid.uuid3(self.vuid, f"volvopy.{self.api}"))
        mf.syslog_trace(f"GUID: {self.guid}", False, self.debug)


if __name__ == "__main__":
    DEBUG = True
    a = Extended_Vehicle(debug=DEBUG)
    print(a.get_all())

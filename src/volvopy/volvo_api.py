#!/usr/bin/env python3

import json
import os
import random
import uuid

import mausy5043_common.funfile as mf
import requests

import volvopy.settings.constants as vc

DEBUG = False
HERE = os.path.realpath(__file__).split("/")
MYID = HERE[-1]


# Token for testing: https://developer.volvocars.com/apis/docs/test-access-tokens/#demo-car

__UUID__ = uuid.UUID("{FACADE00-289C-11EE-8000-6AB05A49B93D}")  # Application UUID


class VolvopyException(Exception):
    """Base class for all volvopy exceptions"""

    def __init__(self, message, api):
        self.message = message
        self.api = api

    def __str__(self):
        msg = f"(volvopy.{self.api}) {self.message}"
        return msg


class VolvoAPI:
    """Base Class to connect and interact with the Volvo Energy API.

    ref.: https://developer.volvocars.com/apis/
    """

    def __init__(self, debug=False):
        self.debug = debug  # flag for debugging
        self.api_key = vc.API_KEY[round(random.random())]  # nosec
        # select one of the keys for use
        # For testing: a DEMO token is needed, which will be valid for 1 hr and can be
        # generated here: https://developer.volvocars.com/apis/docs/test-access-tokens/#demo-car
        self.vin = vc.API_VIN  # The VIN number of the car
        self.uuid = __UUID__  # application UUID
        mf.syslog_trace(f"          UUID: {str(self.uuid)}", False, self.debug)
        # construct an application-wide instance-specific UUID
        self.vuid = uuid.uuid3(self.uuid, "volvopy")
        mf.syslog_trace(f"          VUID: {str(self.vuid)}", False, self.debug)

        self.api = ""
        self.api_token = None
        self.api_spec = {}
        self.guid = (
            "deadd00d-dead-d00d-dead-badbadbadbad"  # placeholder for a API-specific UUID
        )

    def get_all(self):
        """GET all paths"""
        result = []
        vin = self.vin  # noqa  # for use in the eval line
        resource = "none"  # noqa  # for use in the eval line
        id = "none"  # noqa  # for use in the eval line
        base_url = f"{self.api_spec['servers'][0]['url']}"
        for path in self.api_spec["paths"]:
            if "resources" in path:
                print("*********GOTCHA******", path)
            if "requests" in path:
                print("*********GOTCHA******", path)
            try:
                if self.api_spec["paths"][path]["get"]:
                    # get the 'Accept' entry from the specification
                    accept = list(
                        self.api_spec["paths"][path]["get"]["responses"]["200"]["content"]
                    )[
                        0
                    ]  # construct the headers
                    headers = {
                        "Content-type": "application/json",
                        "Accept": f"{accept}",
                        "authorization": f"Bearer {self.api_token}",
                        "vcc-api-key": self.api_key,
                        "vcc-api-operationId": self.guid,
                    }
                    # construct the URL
                    try:
                        url = eval(f"f'{base_url}{path}'")  # nosec

                        mf.syslog_trace(f"---\nGETting {url} ", False, self.debug)
                        response = requests.get(url, headers=headers, timeout=10)
                        content = json.loads(response.content)

                        mf.syslog_trace("Result data: ", False, self.debug)
                        for _key in content:
                            if _key in [
                                "data",
                                "resources",
                                "vehicles",
                                "requests",
                            ] and isinstance(content[_key], dict):
                                for _data_key in content[_key]:
                                    mf.syslog_trace(
                                        f"d      {_data_key} :: {content[_key][_data_key]}",
                                        False,
                                        self.debug,
                                    )
                            if _key in [
                                "data",
                                "resources",
                                "vehicles",
                                "requests",
                            ] and isinstance(content[_key], list):
                                for _d in content[_key]:
                                    # for _data_key in _d:
                                    mf.syslog_trace(
                                        f"d      {_key} :: {_d}",
                                        False,
                                        self.debug,
                                    )
                            else:
                                mf.syslog_trace(
                                    f"k   {_key} :: {content[_key]}", False, self.debug
                                )
                        result.append(content)
                    except json.decoder.JSONDecodeError as her:
                        print("Invalid response from server.")
                        pass
                    except Exception as her:
                        # Non-anticipated exceptions must be raised to draw attention to them.
                        reraise = VolvopyException(f"{her}", self.api)
                        print("text:", response.text)
                        raise  # reraise from her
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


class Connected_Vehicle(VolvoAPI):
    """Class to connect and interact with the Volvo Connected Vehicle API.

    ref.: https://developer.volvocars.com/apis/connected-vehicle/v1/specification/
    """

    def __init__(self, debug=False):
        super().__init__(debug=debug)

        self.api = "connected"
        self.api_token = vc.API_TOKEN[self.api]
        self.api_spec = vc.API_SPECIFICATIONS[self.api]
        self.guid = str(uuid.uuid3(self.vuid, f"volvopy.{self.api}"))
        mf.syslog_trace(f"Connected GUID: {self.guid}", False, self.debug)


class Energy(VolvoAPI):
    """Class to connect and interact with the Volvo Energy API.

    ref.: https://developer.volvocars.com/apis/energy/v1/specification/
    """

    def __init__(self, debug=False):
        super().__init__(debug=debug)

        self.api = "energy"  # Name of the API.
        self.api_token = vc.API_TOKEN[self.api]
        self.api_spec = vc.API_SPECIFICATIONS[self.api]
        self.guid = str(uuid.uuid3(self.vuid, f"volvopy.{self.api}"))
        mf.syslog_trace(f"   Energy GUID: {self.guid}", False, self.debug)


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
        mf.syslog_trace(f" Extended GUID: {self.guid}", False, self.debug)


class Location(VolvoAPI):
    """Class to connect and interact with the Volvo Location API.

    ref.: https://developer.volvocars.com/apis/location/v1/specification/
    """

    def __init__(self, debug=False):
        super().__init__(debug=debug)

        self.api = "location"
        self.api_token = vc.API_TOKEN[self.api]
        self.api_spec = vc.API_SPECIFICATIONS[self.api]
        self.guid = str(uuid.uuid3(self.vuid, f"volvopy.{self.api}"))
        mf.syslog_trace(f" Location GUID: {self.guid}", False, self.debug)


if __name__ == "__main__":
    # for testing purposes only
    DEBUG = True
    a = Location(debug=DEBUG)
    car_loc = a.get_all()

    a = Extended_Vehicle(debug=DEBUG)
    car_xtnd = a.get_all()

    a = Energy(debug=DEBUG)
    car_nrg = a.get_all()

    a = Connected_Vehicle(debug=DEBUG)
    car_cnct = a.get_all()

    print("\n----location---")
    for path_result in car_loc:
        print(path_result)
    print("\n----energy----")
    for path_result in car_nrg:
        print(path_result)
    print("\n----connected----")
    for path_result in car_cnct:
        print(path_result)
    print("\n----extended----")
    for path_result in car_xtnd:
        print(path_result)

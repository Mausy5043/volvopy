#!/usr/bin/env python3

import os

from volvopy import connected as car_con
from volvopy import energy as car_nrg
from volvopy import extended as car_xtnd
from volvopy import location as car_loc

DEBUG = True
HERE = os.path.realpath(__file__).split("/")
MYID = HERE[-1]

example_con = car_con.Connected_Vehicle(debug=DEBUG)
example_con.get_all()
example_nrg = car_nrg.Energy(debug=DEBUG)
example_nrg.get_all()
example_xtnd = car_xtnd.Extended_Vehicle(debug=DEBUG)
example_xtnd.get_all()
example_loc = car_loc.Location(debug=DEBUG)
example_loc.get_all()

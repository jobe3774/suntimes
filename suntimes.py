#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Calculate the times for sunrise, sun's culmination and sundown for yesterday, today and tomorrow 
#  for given geographical coordinates.
#
#  The calculation is based on SunMoon.py by Michael Dalder, which in turn is a port of Arnold Barmettler's JavaScript. 
#  You can find both on https://lexikon.astronomie.info/java/sunmoon/.
#  
#  License: MIT
#  
#  Copyright (c) 2019 Joerg Beckers

import argparse

from datetime import datetime, timedelta

from raspend.application import RaspendApplication
from raspend.utils import dataacquisition as DataAcquisition

from SunMoon import SunMoon

class SunTimes():
    def calc(self, dateStr, longitude, latitude):
        try:
            calcDate = datetime.strptime(dateStr, "%Y-%m-%d")
        except ValueError as e:
            return e

        sunMoon = SunMoon(float(longitude), float(latitude), calcDate)
        sunRiseSet = sunMoon.GetSunRiseSet()

        sunTimesDict = { "SunTimes" : {"Sunrise": "--:--", "Culmination" : "--:--", "Sunset": "--:--", "Date": ""} }

        sunTimesDict["SunTimes"]["Date"] = dateStr
        sunTimesDict["SunTimes"]["Sunrise"] = sunRiseSet[0]
        sunTimesDict["SunTimes"]["Culmination"] = sunRiseSet[1]
        sunTimesDict["SunTimes"]["Sunset"] = sunRiseSet[2]

        return sunTimesDict

def main():

    # Check commandline arguments.
    cmdLineParser = argparse.ArgumentParser(prog="suntimes", usage="%(prog)s [options]")
    cmdLineParser.add_argument("--port", help="The port the server should listen on.", type=int, required=True)

    try: 
        args = cmdLineParser.parse_args()
    except SystemExit:
        return

    sunTimesApp = RaspendApplication(args.port)

    sunTimesApp.addCommand(SunTimes().calc)

    sunTimesApp.run()

if __name__ == "__main__":
    main()

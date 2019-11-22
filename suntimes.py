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
from datetime import datetime, timedelta, timezone
from raspend import RaspendApplication
from SunMoon import SunMoon

def to_bool(value):
    """
       Converts 'something' to boolean. Raises exception for invalid formats
           Possible True  values: 1, True, "1", "TRue", "yes", "y", "t"
           Possible False values: 0, False, None, [], {}, "", "0", "faLse", "no", "n", "f", 0.0, ...

       thanks to Petrucio (see https://stackoverflow.com/a/9333816)
    """
    if str(value).lower() in ("yes", "y", "true",  "t", "1"): return True
    if str(value).lower() in ("no",  "n", "false", "f", "0", "0.0", "", "none", "[]", "{}"): return False
    raise Exception('Invalid value for boolean conversion: ' + str(value))

class SunTimes():
    def calc(self, 
             dateStr : "Date formatted as YYYY-MM-DD", 
             longitude : "Longitude of location", 
             latitude : "Latitude of location", 
             asISO : "True: Times will be formatted as ISO8601 (UTC), False: Unix timestamp (UTC)" = False):
        try:
            calcDate = datetime.strptime(dateStr, "%Y-%m-%d")
        except ValueError as e:
            return e

        sunMoon = SunMoon(float(longitude), float(latitude), calcDate)
        sunRiseSet = sunMoon.GetSunRiseSet()

        sunTimesDict = { "SunTimes" : {"Sunrise": 0, "Culmination" : 0, "Sunset": 0} }

        if to_bool(asISO):
            sunTimesDict["SunTimes"]["Sunrise"] = datetime.fromtimestamp(sunRiseSet[0], tz=timezone.utc).isoformat()
            sunTimesDict["SunTimes"]["Culmination"] = datetime.fromtimestamp(sunRiseSet[1], tz=timezone.utc).isoformat()
            sunTimesDict["SunTimes"]["Sunset"] = datetime.fromtimestamp(sunRiseSet[2], tz=timezone.utc).isoformat()
        else:
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

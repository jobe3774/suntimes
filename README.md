# suntimes
A [raspend](https://github.com/jobe3774/raspend) based application serving the times for sunrise, sun's culmination and sunset.

Start the server:
```
$ python3 suntimes.py --port 8080
```
Then you can request the sun times for a given location at a given date:

```
http://localhost:8080/cmd?name=SunTimes.calc&dateStr=2019-11-26&longitude=13.413215&latitude=52.521918&asISO=True
```
The above request delivers the sun times for Berlin on Nov. 26th 2019. All times returned are in UTC.

``` json
{
  "SunTimes": {
    "Sunrise": "2019-11-26T06:46:00+00:00", 
    "Culmination": "2019-11-26T10:54:00+00:00", 
    "Sunset": "2019-11-26T15:01:00+00:00"
  }
}
```

The calculation is based on SunMoon.py by Michael Dalder, which in turn is a port of Arnold Barmettler's JavaScript. You can find both [here](https://lexikon.astronomie.info/java/sunmoon/).
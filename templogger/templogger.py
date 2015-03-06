import pywapi
import time
import subprocess

#get the outside temp
#to get the local station go to http://w1.weather.gov/xml/current_obs/seek.php 
#and get the 4 letter station, input below
noaa_result = pywapi.get_weather_from_noaa('KKKK')

#Get the USB temp, retry a couple of times if we can't query the device
trycount = 0
while trycount < 3:

    try:
        indoor_result = float(subprocess.check_output("/usr/bin/temperv14 -f", shell=True))
    except subprocess.CalledProcessError:
        indoor_result = 'failure'

    if type(indoor_result).__name__ == 'str':
        trycount += 1
        print ('Cannot query USB thermometer.  Trying again.../')
    else:
        break


#Get the current time
time = time.strftime("%m/%d/%y @ %H:%M")

#Display the Temps
print ('Outside:', time, noaa_result['temp_f'], 'F')
if trycount == 3:
        print ('Inside: unknown')
else:
        print ('Inside:', time, (indoor_result-20), 'F')
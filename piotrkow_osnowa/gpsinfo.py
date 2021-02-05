import os
from GPSPhoto import gpsphoto

path = input("PATH:\n> ")

for subdir, dirs, files in os.walk(path):
    for file in files:
        if "35-" in file:
            filepath = os.path.join(subdir, file)
            data = gpsphoto.getGPSData(filepath)
            if data:
                print(f"{data['Latitude']}___{data['Longitude']}___{filepath}")

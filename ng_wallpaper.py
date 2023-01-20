#!/usr/bin/python3
from datetime import datetime
import requests
from pathlib import Path
import os
import subprocess
from PIL import Image

NG_base_url = 'http://www.nationalgeographic.com/photography/photo-of-the-day/\
_jcr_content/.gallery.'

def getImageTitleUrl():
	today = datetime.now()
	year = str(today.year)
	month = f'0{str(today.month)}' if today.month < 10 else str(today.month)
	url = f"{NG_base_url}{year}-{month}.json"
	print(url);

	r = requests.get(url)

	if r.status_code == 200:
			data = r.json()
			if 'items' not in data: return ""
			current_photo = data['items'][0]['image']
		#	if 'renditions' in current_photo:
		#		return current_photo["title"], current_photo['renditions']['2048']
			return current_photo["title"],current_photo["uri"]
	return ""

title, url = getImageTitleUrl();   

if len(title) == 0 or len(url) == 0:
	print("failed to retrieve!")
	exit();

destination_file = f'{Path.home()}/Pictures/NationalGeographics/{title.replace(" ","_")}.jpg'
if os.path.isfile(destination_file):
	print("esiste già")
#	exit()
else:
    with open(destination_file, 'wb') as f:
        f.write(requests.get(url).content)
    #png conversion
    png_dest = destination_file.replace(".jpg",".png")
    subprocess.run(["convert","-scale","3840x2160^",destination_file,png_dest])
    destination_file = png_dest

            #os.system(f"feh --bg-scale {destination_file}")
result = subprocess.run(['feh', '--bg-scale',destination_file], stdout=subprocess.PIPE)
print(result.stdout)


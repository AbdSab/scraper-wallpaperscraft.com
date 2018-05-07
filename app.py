from bs4 import BeautifulSoup
import shutil
import requests
import csv
import re
import time

#Prams
proxy = {'https':'35.188.216.229:80'}

for page in range(59,159):
	#Link
	print "Page : " + str(page) + " scarped"
	page_link ='https://wallpaperscraft.com/catalog/anime/800x1280'
	
	if page != 1:
		page_link ='https://wallpaperscraft.com/catalog/anime/800x1280/page'+ str(page)
	
	page_response = requests.get(page_link, timeout=5, proxies=proxy)
	page_content = BeautifulSoup(page_response.content, "html.parser",from_encoding="utf-8")
	divs = page_content.find_all('div', {'class': 'wallpaper_pre'})


	for i in divs:
		
		#Data
		thumb         =  'https:' + i.contents[1].contents[1].get('src')
		tags          = i.contents[3].text.replace(", ", "-").encode('utf-8')
		
		global_link   = re.sub('[^A-Za-z0-9]+', '_', tags) + ".jpg"
		file_name     = "thumb/" + global_link
		full_image_path = "wallpaper/" + global_link
		
		
		#Download Thumb
		response = requests.get(thumb, stream=True)
		with open(file_name, 'wb') as out_file:
			shutil.copyfileobj(response.raw, out_file)
		del response
		
		
		#Get Full Image Link
		url = 'https:' + i.find('a').get('href')
		response_fullimage = requests.get(url, timeout=5, proxies=proxy)
		soup = BeautifulSoup(response_fullimage.content, "html.parser")
		
		full_image_link = 'https:' + soup.find('a', {'class': 'wd_zoom'}).find('img').get('src')
		
		#Download Full Image
		response_fullimage_download = requests.get(full_image_link, stream=True, proxies=proxy)
		with open(full_image_path, 'wb') as out_file:
			shutil.copyfileobj(response_fullimage_download.raw, out_file)
		del response_fullimage_download
		
		#Save data
		csv = open('database.csv', 'a')
		row = global_link + ', ' + tags + '\n'
		csv.write(row)
		
	time.sleep(0.1)
	
print "Done :)"
	
	
	
	
	
	

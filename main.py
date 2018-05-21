import re
import requests
import io
import time
import os

import sys
if sys.version_info[0] == 2:  # the tkinter library changed it's name from Python 2 to 3.
    import Tkinter
    tkinter = Tkinter #I decided to use a library reference to avoid potential naming conflicts with people's programs.
else:
    import tkinter
from PIL import Image, ImageTk


image_counter = 0



def showPIL(pilImage):
    root = tkinter.Toplevel()
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.overrideredirect(1)
    root.geometry("%dx%d+0+0" % (w, h))
    root.focus_set()    
    root.bind("<Escape>", lambda e: (e.widget.withdraw(), e.widget.quit()))
    canvas = tkinter.Canvas(root,width=w,height=h)
    canvas.pack()
    canvas.configure(background='black')
    imgWidth, imgHeight = pilImage.size
    if imgWidth > w or imgHeight > h:
        ratio = min(w/imgWidth, h/imgHeight)
        imgWidth = int(imgWidth*ratio)
        imgHeight = int(imgHeight*ratio)
        pilImage = pilImage.resize((imgWidth,imgHeight), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(pilImage)
    imagesprite = canvas.create_image(w/2,h/2,image=image)
    root.update()



def download_image(url, image_name):
	r = requests.get(url, timeout=4.0)
#    if r.status_code != requests.codes.ok:
#        assert False, 'Status code error: {}.'.format(r.status_code)
#
#    with Image.open(io.BytesIO(r.content)) as im:
#        im.save(image_file_path)
#
	if r.status_code == 200:
		f =  open(image_name, 'wb+')
		for chunk in r.iter_content(1024):
			f.write(chunk)
		f.close()
	print('Image downloaded from url: {} and saved to: {}.'.format(url, image_name))

def get_art():

	
	#url = "https://backend.deviantart.com/rss.xml?q=boost%3Apopular+max_age%3A24h+in%3Adigitalart%2Fpaintings%2Ffantasy&amp;type=deviation"
	url = "https://backend.deviantart.com/rss.xml?q=boost%3Ahot+in%3Adigitalart%2Fpaintings%2Flandscapes&amp;type=deviation"
	global image_counter

	response = requests.get(url,timeout = 5.0)
#	print(response.text)
	#urls = re.findall(r'https:\/\/.+\.deviantart.com\/art\/.*(\.png)?', response.text)
	urls = re.findall(r'<media:content\surl="(https:\/\/.*\.deviantart.net\/.*(\.png))?(\.jpg)?".*\/>', response.text)
#	for url in urls:
#		print(url[0])
#		print(url[1])
#		print(url[2] == '')
#
	for url in urls:
		dir_path = os.path.dirname(os.path.realpath(__file__))
		extension = url[1] if url[2] == '' else url[2] 
		image_name = str(image_counter) + extension
		print(image_name)
		print(url)
		
		download_image(url[0], image_name)
		image_counter += 1


def main():
	while True:
		get_art()
		for index in range(0, image_counter + 1):
			image_name = str(index) + ".png"
			im = Image.open(image_name)
			showPIL(im)
			time.sleep(5)
			im.close()

if __name__ == "__main__" :
	main()





#try:
#	response = urllib.urlopen(url, timeout = 5)
#	urls = re.findall(r'https:\/\/.+\.deviantart.com\/art\/.*(\.png)?', response)
#	for url in urls:
#	try:
#		image = urllib.urlopen(url, timeout = 5)
#		f = open("./" + image_counter + ".png", 'w')
#		f.write(image)
#		f.close()
#	except urllib.URLError as e:
#		print(e) 
#
#except urllib.URLError as e:
#	print(e)
#
#for index in range(0, image_counter + 1):
#	image = Image.open(index + ".jpg")
#	
#

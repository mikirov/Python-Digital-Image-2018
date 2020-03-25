import re
import requests
import io
import time
import os

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
	if r.status_code == 200:
		f =  open(image_name, 'wb+')
		for chunk in r.iter_content(1024):
			f.write(chunk)
		f.close()
	print('Image downloaded from url: {} and saved to: {}.'.format(url, image_name))

def get_art():

	
	url = "https://backend.deviantart.com/rss.xml?q=special%3Add"
	global image_counter

	response = requests.get(url,timeout = 5.0)
	urls = re.findall(r'<media:content\surl=\"(.*?)\".*\/>', response.text)
	for url in urls:
		image_name = str(image_counter) + '.jpg'
		download_image(url, image_name)
		image_counter += 1


def main():
	while True:
		get_art()
		for index in range(0, image_counter + 1):
			image_name = str(index) + ".jpg"
			im = Image.open(image_name)
			showPIL(im)
			time.sleep(5)
			im.close()

if __name__ == "__main__" :
	main()






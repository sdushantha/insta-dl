try:
        from time import sleep
        import requests, argparse, urllib.request, os, tkinter
except ImportError:
	print("You need the module requests to run this!")
	exit()

window = tkinter.Tk()

do_download_videos = tkinter.IntVar(value=0)

def download_images(username):
	request_url = "https://www.instagram.com/"+username+"/media/"
	
	headers = {
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0'
	}
	
	params = {'max_id': '0'}
	
	more_available = True
	
	make_folder(entry.get())
	
	while more_available:
		r = requests.get(request_url, headers=headers, params=params)
		
		try:
			data = r.json()
		except:
			print("Invalid username!")
			os.removedirs(entry.get())
			exit()
		
		for content in data["items"]:
			if content["type"] == "video" and do_download_videos.get() == 1:
				file_url = content["videos"]["standard_resolution"]["url"]
			else:
				file_url = content["images"]["standard_resolution"]["url"]
				
			file_url = file_url.replace("s640x640","s1080x1080")
			
			file_name = file_url.split("/")[-1]
			
			path = entry.get()+"/"+username+"_"+file_name
			if not os.path.isfile(path):
				urllib.request.urlretrieve(file_url,path)
				print("Downloaded: "+path)
				sleep(0.5)
		print("--------------Completed--------------")		
				
		more_available = data["more_available"]
		
		new_max_id = data["items"][len(data["items"]) - 1]["id"]
		
		params = {'max_id': new_max_id}
		
		if more_available:
			print("Getting next page of images with maximum id: "+new_max_id)

def action():
        download_images(entry.get())
        
#Make folder with given username
def make_folder(username):

	try:
		mkdir = os.makedirs(username)
	except OSError:
		print("Folder with that username already exists!")
		exit()

#Building the UI		
window.configure(background="grey90")
window.title("insta-dl")
window.geometry("300x200")
window.resizable(False, False)

entry = tkinter.Entry(window)
entry.place(x=70,y=68)
entry.configure(highlightbackground="grey90")

button = tkinter.Button(window, text="Download")
button.place(x=110,y=120)
button.configure(command=lambda:action(),highlightbackground="grey90")

video_checkbox = tkinter.Checkbutton(window, text="Download Video", variable=do_download_videos, bg="grey90")
video_checkbox.place(x=95,y=150)

notice = tkinter.Label(window, text="insta-dl is not affiliated with Instagram",
                       fg="grey60",bg="grey90")
notice.place(x=30, y=180)

window.mainloop()

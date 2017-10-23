try:
        from tkinter.ttk import *
        import requests, argparse, urllib.request, os, tkinter
except ImportError:
	print("You need the module requests to run this!")
	
def download_images(username):
	request_url = "https://www.instagram.com/"+username+"/media/"
	
	headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0'
}

	r = requests.get(request_url, headers=headers)
	
	try:
		data = r.json()
	except:
		print("Invalid username!")
		exit()
	make_folder(entry.get())

	num=10
	for content in data["items"]:
		file_url = content["images"]["standard_resolution"]["url"]
		file_url = file_url.replace("s640x640","s1080x1080")
 
		file_name = file_url.split("/")[-1]
		
		path = entry.get()+"/"+file_name
		urllib.request.urlretrieve(file_url,path)
		print("Downloaded: "+path)

def action():
        download_images(entry.get())
        
#Make folder wiht user's username
def make_folder(username):

	try:
		mkdir = os.makedirs(username)
	except OSError:
		print("Folder with that username already exists!")
		exit()

#Biulding the UI		
window = tkinter.Tk()
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

notice = tkinter.Label(window, text="insta-dl is not affiliated with Instagram",
                       fg="grey60",bg="grey90")
notice.place(x=30, y=180)

window.mainloop()

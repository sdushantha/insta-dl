from time import sleep
import requests, urllib, os, json, urllib.request
try:
  import tkinter
except ImportError:
  import Tkinter as tkinter

__version__ = "v.0.2.6"

window = tkinter.Tk()


def download_single(url):
    url = url.split("?")[0] + "media"

    error = 1
    
    # Some sort of magic happens here
    while error:
      try:
        req = urllib.request.urlopen(url)
        error -=1
      except:
        print("\033[91mInvalid url!\033[0m")
        return None

    file_url = req.geturl()
    
    # Instagram uses [p]ixle or [s]ize
    file_url = file_url.replace("p320x320","p1080x1080")
    file_url = file_url.replace("s320x320","s1080x1080")

    file_name = file_url.split("/")[-1]

    folder_name = "single_image"
    path = folder_name + "/" + file_name

    try:
        os.makedirs(folder_name)

    except:
        pass
    
    urllib.request.urlretrieve(file_url, path)
    print("Downloaded: " + path)


def download_bulk(username):
  request_url = "https://www.instagram.com/" + username + "?__a=1"
  more_available = True
  end_cursors = []

  headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0'
  }

  make_folder(entry.get()) # makes folder with given username

  while more_available:
    if not end_cursors:
      response = requests.get(request_url, headers=headers)
    
    else:
      response = requests.get(request_url + "&max_id={}".format(end_cursors[-1]))

    try:
      data = response.json()
    
    except:
      print("\033[91mInvalid username!\033[0m")
      os.removedirs(entry.get())
      break;

    for node in data["user"]["media"]["nodes"]:
      # Cant access video url anymore
      # if src["is_video"] and do_download_videos.get() == 1:
      #   file_url = src["videos"]["standard_resolution"]["url"]
      # else:
      file_url = node["display_src"]
      file_url = file_url.replace("s640x640","s1080x1080")
      file_name = file_url.split("/")[-1]

      path = entry.get() + "/" + username + "_" + file_name
      
      if not os.path.isfile(path):
        
        try:
          urllib.request.urlretrieve(file_url, path)
          print("Downloaded: "+path)
          sleep(0.5)
        
        except:
          print("\033[91m----Skipping this image----\033[0m")

    more_available = data["user"]["media"]["page_info"]["has_next_page"]

    new_max_id = data["user"]["media"]["page_info"]["end_cursor"]
    end_cursors.append(new_max_id)

    if more_available:
      print("\033[92mGetting next page of images with maximum id: " + new_max_id + "\033[0m")
    print("\033[92m--------------Completed--------------\033[0m")


def action():
  download_type = ""
  home_url = "https://"

  if home_url in entry.get():
      download_type = "url"

  if download_type != "url":
      download_bulk(entry.get())

  else:
      download_single(entry.get())

# Make folder with given username
def make_folder(username):
  try:
    os.makedirs(username)
  except OSError:
    os.system("rm -rf " + username)
    os.makedirs(username)

# Building the UI
window.configure(background="grey90")
window.title("insta-dl " + __version__)
window.geometry("300x200")
window.resizable(False, False)

entry = tkinter.Entry(window)
entry.place(x=70,y=68)
entry.configure(highlightbackground="grey90")

button = tkinter.Button(window, text="Download")
button.place(x=110,y=120)
button.configure(command=lambda:action(), highlightbackground="grey90")

notice = tkinter.Label(window, text="insta-dl is not affiliated with Instagram",
                       fg="grey60",bg="grey90")
notice.place(x=30, y=180)

window.mainloop()

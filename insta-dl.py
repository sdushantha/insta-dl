try:
	import urllib2, urllib, argparse
	from json import load
	from os import makedirs
except ImportError:
	print("Python 3 not supported!")
	exit()

def download_images():
	request_url = "https://www.instagram.com/"+args.username+"/media/"

	try:
		json_obj = urllib2.urlopen(request_url)
	except:
		print("Invalid username!")

	data = load(json_obj)
	make_folder()
	for content in data["items"]:
		file_url = content["images"]["standard_resolution"]["url"]
		
		file_name = file_url.replace("https://scontent-arn2-1.cdninstagram.com/","")
		file_name = file_name.replace("https://instagram.fsvg1-1.fna.fbcdn.net/","")
		file_name = file_name.replace("/","")
		
		path = args.username+"/"+file_name
		urllib.urlretrieve(file_url,path)
		print("Downloaded: "+path)

def make_folder():

	try:
		mkdir = makedirs(args.username)
	except OSError:
		print("ERROR: Folder with that username already exists!")
		exit()

parser = argparse.ArgumentParser(description='Instagram Image Downloader')
parser.add_argument('-u', '--username', type=str, metavar='', required=True, help='The username of the the instagram account')
args = parser.parse_args()
download_images()
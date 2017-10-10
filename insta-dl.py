try:
	import urllib2, urllib, argparse
	from json import load
	from os import makedirs
except ImportError:
	print("\033[91mPython 3 not supported!\033[0m")
	exit()

def download_images():
	request_url = "https://www.instagram.com/"+args.username+"/media/"

	try:
		json_obj = urllib2.urlopen(request_url)
	except:
		print("\033[91mInvalid username!\033[0m")

	data = load(json_obj)
	make_folder()
	for content in data["items"]:
		file_url = content["images"]["standard_resolution"]["url"]
		
		file_name = file_url.split("/")[-1]
		
		path = args.username+"/"+file_name
		urllib.urlretrieve(file_url,path)
		print("Downloaded: "+path)

def make_folder():

	try:
		mkdir = makedirs(args.username)
	except OSError:
		print("\033[91mFolder with that username already exists!\033[0m")
		exit()

parser = argparse.ArgumentParser(description='Instagram Image Downloader')
parser.add_argument('-u', '--username', type=str, metavar='', required=True, help='The username of the the instagram account')
args = parser.parse_args()
download_images()

try:
	import requests, argparse
	import urllib.request
	from os import makedirs
except ImportError:
	print("\033[91mYou need the module requests to run this!\033[0m")

def download_images():
	request_url = "https://www.instagram.com/"+args.username+"/media/"

	headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0'
}

	r = requests.get(request_url, headers=headers)
	
	try:
		data = r.json()
	except:
		print("\033[91mInvalid username!\033[0m")
		exit()
	make_folder()
	
	for content in data["items"]:
		file_url = content["images"]["standard_resolution"]["url"]
		
		file_name = file_url.split("/")[-1]
		
		path = args.username+"/"+file_name
		urllib.request.urlretrieve(file_url,path)
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

import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import colorama
import os
import shutil

# init the colorama module
colorama.init()
GREEN = colorama.Fore.GREEN
GRAY = colorama.Fore.LIGHTBLACK_EX
RESET = colorama.Fore.RESET
YELLOW = colorama.Fore.YELLOW

# Variables globales
pages = {}
total_urls_visited = 0

# Source :
# https://thepythoncode.com/article/extract-all-website-links-python

def get_links(url,choice="all"):
	"""
	Returns all URLs that is found on `url` in which it belongs to the same website
	"""

	urls = set()
	internal_urls = set()
	external_urls = set()

	# domain name of the URL without the protocol
	domain_name = urlparse(url).netloc
	try :
		soup = BeautifulSoup(requests.get(url).content, "html.parser")
	except :
		raise ValueError("Problem with URL")
	
	for a_tag in soup.findAll("a"):
		href = a_tag.attrs.get("href")
		href = urljoin(url, href)
		parsed_href = urlparse(href)
		# remove URL GET parameters, URL fragments, etc.
		href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
		if filter(href,url):
			if domain_name not in href:
				if href not in external_urls:
					external_urls.add(href)
			elif href not in internal_urls:
				internal_urls.add(href)
			urls.add(href)

	if choice=="all":
		return url
	elif choice=="intern":
		return internal_urls
	elif choice=="extern":
		return external_urls
	else :
		raise ValueError("Choice must be \"all\", \"intern\" or \"extern\"")
	

def filter(href,url):
	if href==url:
		return False
	if href in pages :
		return False
	filters = ["Category","Wikipedia","ISBN","Special","File","index","Aide","Portail","Glossaire","Recherche","Wikip%C3%A9dia","Accueil","Fichier"]
	res = True
	for filter in filters :
		if filter in href :
			res = False
			break
	return res

def get_title(url):
	segments = url.split('/')
	return segments[-1].replace("_"," ")

def add_to_pages(url,urls):
	text = ""
	for link in urls:
		text+="[["+str(get_title(link))+"]]\n"
	global pages
	pages[url] = text
	


def crawl(url, max_urls):
	"""
	Crawls a web page and extracts all links.
	You'll find all links in `external_urls` and `internal_urls` global set variables.
	params:
		max_urls (int): number of max urls to crawl
	"""
	global total_urls_visited
	total_urls_visited += 1
	print("- Crawling: "+ url)
	links = get_links(url,"intern")
	add_to_pages(url,links)
	for link in links:
		if total_urls_visited > max_urls:
			break
		crawl(link, max_urls=max_urls)
	

if __name__ == "__main__":
	max_urls=100
	crawl("https://www.youtube.com/",max_urls)
	shutil.rmtree("Logs")
	os.makedirs("Logs")
	for key in pages :
		with open("logs/"+get_title(key)+".md","w",encoding="UTF8") as file:
			file.write(pages[key])


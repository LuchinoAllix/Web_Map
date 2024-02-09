import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import os
import shutil

# Variables globales
pages = {}
total_urls_visited = 0
filters =[]

# Source :
# https://thepythoncode.com/article/extract-all-website-links-python

def get_links(url,choice="all"):
	"""
	Obtient tous les liens d'une page web

	Paramètres :
	url (String) : le lien de la page
	Choice (String) : "all" si on veut tous les liens, "intern" si on 
		veut que les liens intern et "extern" sinon

	Retour :
	(set de String) : set des liens
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
	"""
	Filtre quel liens on veut garder, on retire ceux qu'on a déjà, 
	ceux qui sont vides ou ceux qui contienne un mot indésirable (via la variable global filters) 

	Paramètres :
	href (String) : le lien dans la page
	url (String) : le lien de la page

	Retour :
	(Bool) True si on garde le lien, False sinon
	"""

	if href==url or href==" " or href=="" or href in pages:
		return False
	global filters
	res = True
	for filter in filters :
		if filter in href :
			res = False
			break
	return res

def get_title(url):
	"""
	Extrait le titre d'une page web via son url

	Paramètres :
	url (String) : le lien de la page

	Retour :
	(String) : le titre de la page
	"""
	segments = url.split('/')
	return segments[-1].replace("_"," ")

def add_to_pages(url,urls):
	"""
	Crée un noeud url et rajoute les urls dans ses liens

	Paramètres :
	url (String) : le lien de la page
	urls (String) : les liens sur la page url

	Retour :
	None (effet de bord sur "pages")
	"""
	text = ""
	for link in urls:
		text+="[["+str(get_title(link))+"]]\n"
	global pages
	pages[url] = text

def crawl(url, max_urls):
	"""
	Cherche tous les liens sur une page et cherche tous les liens sur chacun des liens,
	jusqu'a ce que tous les liens ont été visité ou que max_urls est atteint.
	Rajoute tous les liens dans la structure de données "pages".

	Paramètres :
	url (String) : le lien de la page
	max_urls (int) : le nombre maximum de liens à regarder

	Retour :
	None (effet de bord sur "pages" via "add_to_pages()")
	"""
	global total_urls_visited
	total_urls_visited += 1
	print("- Crawling: "+ url)
	links = get_links(url,"intern")
	add_to_pages(url,links)
	for link in links:
		if total_urls_visited > max_urls:
			break
		crawl(link, max_urls)
	
	
if __name__ == "__main__":
	max_urls=100
	crawl("https://www.youtube.com/",max_urls)
	shutil.rmtree("Logs")
	os.makedirs("Logs")
	for key in pages :
		with open("logs/"+get_title(key)+".md","w",encoding="UTF8") as file:
			file.write(pages[key])


from django.http import HttpResponse
import re
import requests
from html.parser import HTMLParser
from django.shortcuts import render

img=[]
output=[]
class Parser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag=="img":
            img.append(dict(attrs)["src"])

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
def fetchData(link):
	data = requests.get(link,headers=hdr)
	return data

parser = Parser()
def index(request,url=None,dept=None):
	output.clear()
	url = request.GET.get('name')
	dept = request.GET.get('level')
	r=requests.get(url,allow_redirects=False,headers=hdr)
	if dept == '1':
	  urls = re.findall(r'<loc>(.*?)</loc>',r.text)
	  output.append(urls)
	elif dept == '2':
		r=fetchData(url)
		links=re.findall(r'<loc>(.*?)</loc>|<image:loc>(.*?)</image:loc>',r.text) 	
		output.append(links)
	elif dept=='3':
	    im = requests.get(url,allow_redirects=False,headers=hdr)
	    parser.img=[]
	    parser.feed(im.text)
	    output.append(img)
	return HttpResponse(output)

from django.http import HttpResponse
import re
import requests
from html.parser import HTMLParser
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
result=[]
class Parser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag=="img":
            result.append(dict(attrs)["src"])

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

def index(request):
	return HttpResponse("Access http://..../data/?name=''&level=''")

@api_view(['GET'])
def get_urls(request,url=None,dept=None):
	result.clear()
	url = request.GET.get('name')
	dept = request.GET.get('level')
	r=fetchData(url)
	if dept == '1':
	  urls = re.findall(r'<loc>(.*?)</loc>',r.text)
	  result.extend(urls)
	elif dept == '2':
		links=re.findall(r'<loc>(.*?)</loc>',r.text)
		ilinks = re.findall(r'<image:loc>(.*?)</image:loc>',r.text)
		urls = links+ilinks
		result.extend(urls)
	elif dept=='3':
	    parser.result=[]
	    parser.feed(r.text)
	    
	return JsonResponse({'urls': result})

from django.http import HttpResponse
import re
import requests
import json
from html.parser import HTMLParser
from django.shortcuts import render
from rest_framework.decorators import api_view # new
from rest_framework.response import Response # new
from rest_framework.reverse import reverse # new
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
@api_view(['GET'])
def index(request,url=None,dept=None):
	output.clear()
	url = request.GET.get('name')
	dept = request.GET.get('level')
	r=fetchData(url)
	if dept == '1':
	  urls = re.findall(r'<loc>(.*?)</loc>',r.text)
	  output.append(urls)
	elif dept == '2':
		links=re.findall(r'<loc>(.*?)</loc>',r.text)
		ilinks = re.findall(r'<image:loc>(.*?)</image:loc>',r.text)
		out = links+ilinks
		output.append(out)
	elif dept=='3':
	    parser.img=[]
	    parser.feed(r.text)
	    output.append(img)
	return Response(json.dumps({'result':output}))


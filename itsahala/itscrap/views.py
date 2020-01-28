import requests
from bs4 import BeautifulSoup
import time
from django.shortcuts import render
from random import randint
import re
'''
########    Stipend - main field NAME
########    inside table-responsive class get the table then in thead get Stipend and inside tbody 3rd td is
########    our target
########    important tip for getting url is most important becs ease whole process you have to select all filter you want to scrab the website apply those filter on internshala go to 2nd page and copy url to the "URL" variable down there with deleting just a page number 
'''

def index(request):
	# loop init
	c = int(1)
	p = 1
	mylist = {}
	i = int(0)
	#start loop for get data from desire website
	for p in range(50):#change range accordingly how many page you want to surf
		print('number',p)
		#urls defining
		url = "https://internshala.com/internships/internship-in-bangalore/page-"+str(c)
		c = int(c) + 1
		# print(url)
		response = requests.get(url)
		html = response.content
		# print(html)
		soup = BeautifulSoup(html, "html.parser")
		# print(soup)
		test = soup.findAll('div',attrs={'class','individual_internship'})
		a = None
		for a in test:
			tempin = a.find('td',attrs={'class','stipend_container_table_cell'})
			link = a.find('a',attrs={'class','view_detail_button'})
			if link == None or tempin == None:
				continue
			print('---------------------------------')
			print('salary---->',tempin.text.strip().lower(),'|----|link-> ',link.get('href'))
			f_link = 'https://internshala.com'+link.get('href')
			f_sal = tempin.text.strip()
			f_sal = f_sal.split('/')
			if re.search("-",f_sal[0]) and f_sal:
				f_sal = f_sal[0].split('-')
				print(f_sal[0],"it's inside")
				fal = f_sal[0].lower()
				if re.search("lump",fal) and f_sal:
					f_sal0 = fal.split(' ')
					f_sal0 = int(f_sal0[0])
				else:	
					f_sal0 = int(f_sal[0])
				f_sal1 = f_sal[1]
				if f_sal0 >= 10000:
					i += 1
					mylist.update({i :{ 'sal': str(f_sal0)+"-"+str(f_sal1),'link': f_link}})
				else:
					continue
			print('-------------------------------------------------')
			print(f_sal[0].lower(),'unpaid',f_sal[0].lower(),'Performance Based')
			print('-------------------------------------------------')
			fal = f_sal[0].lower()
			if re.search("lump",fal) or re.search("not provided",fal) and fal :
				continue
			if f_sal[0].lower() == 'unpaid' or f_sal[0].lower() == 'performance based':
				continue
			else:
				print('out '+f_sal[0]+' out side')
				f_salo = int(f_sal[0])
				if f_salo >= 10000:
					i += 1
					mylist.update({i :{ 'sal': f_salo,'link': f_link}})
				else:
					continue
	return render(request, 'dicta/my.html', {'mylist': mylist })
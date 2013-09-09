# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup
import urllib2
import re
import sys
import csv
from slimmer import html_slimmer
from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def urlread(url):
	f = urllib2.urlopen(url)
	p = f.read()
	return p

restaurants = ["tottisalmi", "arcanum", 'assarin-ullakko', 'brygge', 'delica', 'deli-pharma', 'dental', 'macciavelli', 'mikro', 'myssy-silinteri', 'nutritio', 'ruokakello']
restaurants_lunchlists = {}
for restaurant in restaurants:
  #print restaurant
  html = urlread("http://www.unica.fi/fi/ravintolat/" + restaurant +"/")
  html = unicode(html, 'utf-8')
  parsed_html = BeautifulSoup(html)
  #print parsed_html
  #print parsed_html
  try:
    lunchlist = {}
    lunchlist_html = parsed_html.body.find('div', attrs={'class':'menu-list'})
    for days in lunchlist_html.find_all('div', attrs={'class':'accord'}):
	day = days.find('h4').text
	tmp = []
	for lunch in days.find_all('tr'):
	    lunch_name = lunch.find('td', attrs={'class':'lunch'})
	    lunch_limitations = lunch.find('td', attrs={'class':'limitations quiet'})
	    lunch_price = lunch.find('td', attrs={'class':'price quiet'})
	    lunch_limitations = (re.sub('\n', ' ', re.sub('\t', '', lunch_limitations.text))).strip()
	    lunch_price = re.sub('Hinta:', '',(re.sub('\n', ' ', re.sub('\t', '', lunch_price.text)))).strip()
	    tmp.append([lunch_name.text.encode('utf-8'), lunch_limitations.encode('utf-8'), lunch_price.encode('utf-8')])
	lunchlist[day] = tmp
    restaurants_lunchlists[restaurant] = lunchlist
  except:
    pass

for restaurant in restaurants_lunchlists:
  lunchlist = restaurants_lunchlists[restaurant]
  with open('lunchlist/' + restaurant + '.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    writer.writerow(['DAY', 'LUNCH', 'LIMITATIONS', 'PRICE'])
    for day in lunchlist.keys():
      for lunch in lunchlist[day]:
	writer.writerow([day] + [lunch[0]] + [lunch[1]] + [lunch[2]])
  """
  print "Tällä viikolla herkkuruokaa tarjoaa: " + restaurant.capitalize()
  print "\n"
  print "Katsotaanpa mitä hyvää on tarjolla.."
  print "\n"
  for day in lunchlist.keys():
    print day
    print "\n"
    lunches = lunchlist[day]
    for lunch in lunches:
      print lunch[0] + ' - ' + lunch[1]
      print "Hinta " + lunch[2]
      print "\n"
    print "\n"
  print "-------\n"
  """
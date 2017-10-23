"""
Usage:
	train <from> <to> <date> <hour> <minute>

Example:
	train zurich zug 30.10.2017 10 00
"""

'''
https://www.sbb.ch/de/kaufen/pages/fahrplan/fahrplan.xhtml?suche=true&language=de&vias=%5B%22%22%5D&webshopPreviewMode=inactive&von=zurich&nach=zug&viaField1=&datum=Di%2C+24.10.2017&zeit=10%3A00&an=false

'''
import datetime
from docopt import docopt
import re
import requests
from pprint import pprint
from prettytable import PrettyTable
from bs4 import BeautifulSoup

class TrainCollection:

	header='start time, arrival time, duration, change, track'.split(',')
	def __init__(self, available_trains):
		self.available_trains=available_trains

	@property
	def trains(self):
		for item in self.available_trains:
			start_time=item.find_all(class_="mod_timetable_starttime")[0].get_text()
			arrival_time=item.find_all(class_="mod_timetable_endtime")[0].get_text()
			track=item.find_all(class_="mod_timetable_platform")[0].get_text()
			track=re.findall('[0-9]+',track)[0]
			duration=item.find_all(class_="mod_timetable_duration")[0].get_text()
			change=item.find_all(class_="mod_timetable_change")[0].get_text()

			train=[start_time,
				   arrival_time, 
				   duration, change, '\n' + track]
			yield train

	def pretty_print(self):
		pt=PrettyTable()
		pt._set_field_names(self.header)
		for train in self.trains:
			pt.add_row(train)
		print(pt)

dow_dict={0:'Mo', 1:'Di', 2:'Mi',3:'Do',4:'Fr',5:'Sa',6:'So'}

def cli():
	arguments=docopt(__doc__)
	from_station=arguments['<from>']
	to_station=arguments['<to>']
	date=arguments['<date>']
	hour=arguments['<hour>']
	minute=arguments['<minute>']
	dt = datetime.datetime.strptime(date, '%d.%m.%Y')
	dow = dow_dict.get(dt.weekday())

	url="https://www.sbb.ch/de/kaufen/pages/fahrplan/fahrplan.xhtml?suche=true&language=de&von={}&nach=z{}&viaField1=&datum={}%2C+{}&zeit={}%3A{}".format(
		from_station, to_station, dow, date, hour, minute)
	r=requests.get(url, verify=False)
	soup=BeautifulSoup(r.content, 'html.parser')
	available_trains = soup.find_all(class_="mod_accordion_item_heading var_timetable")
	TrainCollection(available_trains).pretty_print()

if __name__ == '__main__':
	cli()

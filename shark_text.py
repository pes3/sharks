import twilio
from twilio.rest import Client
import json
import bs4
import requests
from pprint import pprint

data = json.loads(open('data/secret.json', 'r').read())
# secret.json password storage

def get_elems_from_document(document):
	pass

res = requests.get('http://www.sharkresearchcommittee.com/pacific_coast_shark_news.htm')
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text, 'html.parser')

for i in range(1, 10):

	elems = soup.select('body > div > div > center > table > tr > td:nth-of-type(2) > p:nth-of-type({})'
	.format(i))
	
	if '—' in str(elems):
		v = elems[0].text

		print("{}th element: ".format(i))
		pprint(elems)

accountSID = data['sid']
authToken = data['authToken']
twilioCli = Client(accountSID, authToken)

myTwilioNumber = data['twilioNumber']
myCellPhone = data['myNumber']

message = twilioCli.messages.create(body = 'Warning: Shark sighting off the coast of ' + v + 'Beach !', from_=myTwilioNumber, to=myCellPhone)

import re 
import bs4
import sqlite3
import requests
import textwrap
#parse all of the existing specifed text data from the html page below
res = requests.get('http://www.sharkresearchcommittee.com/pacific_coast_shark_news.htm')
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text, 'html.parser')

news = [p.text.strip() for p in soup.select('h1 ~ p') if p.find('font')]


c = sqlite3.connect('shark.db') #connnect to DB
try: 
    c.execute('''CREATE TABLE
                    mytable (Location        STRING,
                             Date            STRING,
                             Description     STRING)''')
except sqlite3.OperationalError: #i.e. table exists already
    pass

for n in news:
        groups = re.match(r'(.*?)\W+—?\W+On\W+(.*?\d{4})\W*(.*)', n, flags=re.DOTALL) #re to parse out correct parts of the html text
        if not groups:
            continue
        place, date, article = groups[1], groups[2], groups[3]

        c.execute('''INSERT INTO mytable(Location, Date, Description) VALUES(?,?,?)''',
            (place, date, article))
c.commit()
c.closer()

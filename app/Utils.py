from urllib.request import urlopen   #, Request
from dateutil import parser
from datetime import date,timedelta
from app import Constants



global minimalAllowedDateAsStr
minimalAllowedDateAsStr = str(date.today() - timedelta(days=Constants.DELTA)) # change value of global scope variables defined at beginning of file


def date_to_str(pTime):
    dateAsStr = str(parser.parse(pTime).date())
    # format example: '2020-03-25T00:01:00+0200'
    return dateAsStr

def today():
    return str(date.today())


def load_html(request):
    response = urlopen(request)
    html = response.read().decode('utf8')
    return html
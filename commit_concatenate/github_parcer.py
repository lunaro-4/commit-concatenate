import requests
import bs4
import datetime
import time

URL = 'https://github.com/lunaro-4'


def get_data(html):
    soup=bs4.BeautifulSoup(html,'html.parser')
    commits = soup.find_all('td', class_='ContributionCalendar-day')  
    data = dict()
    for date in commits: 
        year, month, day = (int(x) for x in date['data-date'].split('-'))
        date_in_unix = time.mktime(datetime.date(year, month, day).timetuple())
        # for some reason, github calendar grid does count 1 commit more than there actually is
        if int(date['data-level']) >0:
            date['data-level'] = int(date['data-level'])-1
            data[date_in_unix] = str(date['data-level'])
        elif int(date['data-level']) == 0:
            pass

    return data

def parse(url= URL):
    html = requests.get(url)
    if html.status_code == 200:
        data = get_data(html.text)
        return data
    else:
        print('Error', f'html status: {html.status_code}')

if __name__ == '__main__':
    print(parse())

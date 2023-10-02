import requests
import bs4
import datetime

URL = 'https://github.com/lunaro-4'

def get_html(url, params=None):
    r = requests.get(url, params=params)
    return r

def get_data(html):
    soup=bs4.BeautifulSoup(html,'html.parser')
    commits = soup.find_all('td', class_='ContributionCalendar-day')  
    data = {
            0:[],
            1:[],
            2:[],
            3:[],
            4:[],
            5:[],
            6:[],
    }
    for date in commits: 
        year, month, day = (int(x) for x in date['data-date'].split('-'))
        weekday = datetime.date(year, month, day).weekday()
        # for some reason, github calendar grid does count 1 commit more than there actually is
        if int(date['data-level']) >0:
            date['data-level'] = int(date['data-level'])-1
        data[weekday].append([date['data-date'],str(date['data-level'])])

    return data

def parse(url= URL):
    html = get_html(url)
    #print(html)
    if html.status_code == 200:        
        data = get_data(html.text)
        #print(projects.tail(10))
        #projects.to_csv('projects_finale_social.csv', encoding='utf-8-sig')
        return data
    else:
        print('Error', f'html status: {html.status_code}')

if __name__ == '__main__':
    print(parse())

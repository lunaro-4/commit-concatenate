import urllib.request
import json


#### returns data in dictionary of {date_in_unix : number_of_commits}; size is tied to № of active days


DEFAULT_URL = 'https://leetcode-api-faisalshohag.vercel.app/lunaro-4'

def parse(user: str = 'lunaro-4') -> dict:
    with urllib.request.urlopen('https://leetcode-api-faisalshohag.vercel.app/'+ user) as url:
        data = json.load(url)
    data = data['submissionCalendar']
    data_keys = list(data.keys())
    for i in data_keys:
        #data[int(i)- (3*60*60)] = data.pop(i)
        data[int(i)] = data.pop(i)
    return data
if __name__ == '__main__':
    parse()

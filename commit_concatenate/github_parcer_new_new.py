import requests
import datetime
import multiprocessing
import concurrent.futures
import more_itertools

#### returns data in dictionary of {datetime.date : number_of_commits}; size is tied to № of active days


DEFAULT_USER = 'lunaro-4'
BASE_URL = 'https://api.github.com/users/%s/events?per_page=100&page=%d'


def parse_commit(URL: str):
    try:
        response = requests.get(URL)
        if response.status_code == 200:
            # print(response.json().get('commit').get('author').get('date'))
            return response.json().get('commit').get('author').get('date')
    except:
        return ''


# 2024-03-28T12:36:15Z

def git_to_datetime(git_date: str) -> datetime.date | None:
    git_date_fixed = git_date[:git_date.rfind("T")]
    try:
        unix_date = datetime.datetime.strptime(git_date_fixed, '%Y-%m-%d').date()
    except ValueError:
        return None
    return unix_date


def get_data(json) -> dict:
    dates_list = []
    executor = concurrent.futures.ProcessPoolExecutor(10)
    tasks = []
    for event in json:
        if 'commits' in event.get('payload').keys() :
            for commit in event.get('payload').get('commits'):
                # value = parse_commit(commit.get('url'))
                tasks.append(commit)
                # dates_list.append(value)
    # futures = [executor.submit(parse_commit, group) for group in more_itertools.chunked(tasks, 5)]
    dates_list = [executor.submit(parse_commit, commit) for commit in tasks]
    concurrent.futures.wait(dates_list)
    result = {}
    for date in dates_list:
        # await date
        date = git_to_datetime(str(date))
        if date == None:
            continue
        if date in result.keys():
            result[date] += 1
        else:
            result[date] = 1



    # print(dates)
    return result

def merge_dicts(dict1: dict, dict2: dict):
    for key in dict1.keys():
        if key in dict2.keys():
            dict2[key] += dict1[key]
        else:
            dict2[key] = dict1[key]

def parse(user: str = DEFAULT_USER)-> dict:
    page = 1
    response = requests.get(BASE_URL % (user, page))
    json = response.json()
    data = dict()
    while len(json) > 0:
        if response.status_code == 200:
            new_data = get_data(json)
            merge_dicts(new_data, data)
            page += 1
            response = requests.get(BASE_URL % (user, page))
            json = response.json()
        else:
            print('Error', f'html status: {response.status_code}')
            break
    return data

# async def print_this():
#     this = await parse()
#     print(this)

if __name__ == '__main__':
    result = parse()
    print(result)

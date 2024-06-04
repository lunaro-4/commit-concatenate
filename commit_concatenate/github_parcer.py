import requests
import datetime
import multiprocessing
import concurrent.futures
import more_itertools

#### returns data in dictionary of {datetime.date : number_of_commits}; size is tied to № of active days


DEFAULT_USER = 'lunaro-4'
BASE_URL = 'https://api.github.com/users/%s/events?per_page=100&page=%d'

headers = {'Accept': 'application/vnd.github+json'}
def parse_commit_date(URL: str):
    try:
        response = requests.get(URL, headers=headers)
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
    tasks = parse_links_from_json(json)

    # futures = [executor.submit(parse_commit_date, group) for group in more_itertools.chunked(tasks, 5)]
    dates_list = [executor.submit(parse_commit_date, commit) for commit in tasks]
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
    return result

def merge_dicts(dict1: dict, dict2: dict):
    for key in dict1.keys():
        if key in dict2.keys():
            dict2[key] += dict1[key]
        else:
            dict2[key] = dict1[key]

def parse_links_from_json(json):
    links = []
    for event in json:
        if 'commits' in event.get('payload').keys() :
            for commit in event.get('payload').get('commits'):
                links.append(commit.get('url'))
    return links

def parse_page_response(user: str | None,
                       page: int | None,
                        request_session: requests.Session | None,
                       URL: str = BASE_URL):
    if request_session != None:
        response = request_session.get(URL)
    else:
        response = requests.get(URL % (user, page), headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print('Error', f'html status: {response.status_code}')
        raise Exception

def parse(user: str = DEFAULT_USER, URL: str = BASE_URL)-> dict:
    page = 1
    response = requests.get(URL % (user, page), headers=headers)
    if response.status_code != 200:
        print('Error', f'html status: {response.status_code}')
        return {}
    json = response.json()
    data = dict()
    while len(json) > 0:
        new_data = get_data(json)
        merge_dicts(new_data, data)
        page += 1
        json = parse_page_response(user=user, page=page, URL=URL)
    return data

# async def print_this():
#     this = await parse()
#     print(this)

if __name__ == '__main__':
    result = parse()
    print(result)

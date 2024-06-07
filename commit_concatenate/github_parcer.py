from time import sleep
from django.core.handlers.base import logging # type: ignore[attr-defined]
import requests
import datetime
import concurrent.futures

logger = logging.getLogger("logger")

#### returns data in dictionary of {datetime.date : number_of_commits};
#### size is tied to № of active days

MAX_TRIES = 5

DEFAULT_USER = 'lunaro-4'
BASE_URL = 'https://api.github.com/users/%s/events?per_page=100&page=%d'
headers = {'Accept': 'application/vnd.github+json'}



def parse_commit_date(
    URL: str, requests_session: requests.Session | None = None
) -> str:
    json = parse_page_response(
        URL=URL, user=None, page=None, request_session=requests_session
    )
    if isinstance(json, dict):
        parsed: str = json.get("commit", {}).get("author", {}).get("date")
        return parsed
    else:
        logger.error(f"parse_page_response returned\
                         {type(json)} while resolving {URL}")
        return ""


def git_to_datetime(git_date: str) -> datetime.date | None:
    git_date_fixed = git_date[: git_date.rfind("T")]
    try:
        unix_date = datetime.datetime.strptime(
            git_date_fixed, "%Y-%m-%d"
        ).date()
    except ValueError:
        return None
    return unix_date


def get_data(
    json: list[dict], requests_session: requests.Session | None = None
) -> dict:
    dates_list = []
    executor = concurrent.futures.ProcessPoolExecutor(10)
    tasks = parse_links_from_json(json)
    dates_list = [
        executor.submit(parse_commit_date, commit, requests_session)
        for commit in tasks
    ]
    concurrent.futures.wait(dates_list)
    result: dict = {}
    for git_date in dates_list:
        datetime_date = git_to_datetime(str(git_date.result()))
        if datetime_date is None:
            continue
        if datetime_date in result.keys():
            result[datetime_date] += 1
        else:
            result[datetime_date] = 1
    return result


def merge_dicts(dict1: dict, dict2: dict) -> dict:
    for key in dict1.keys():
        if type(key) != datetime.date:
            print(type(key), "  ", key)
            raise Exception
        if key in dict2.keys():
            dict2[key] += dict1[key]
        else:
            dict2[key] = dict1[key]
    return dict2


def parse_links_from_json(json: list) -> list:
    links = []
    for event in json:
        if "commits" in event.get("payload").keys():
            for commit in event.get("payload").get("commits"):
                links.append(commit.get("url"))
    return links


def try_request(
    user: str | None,
    page: int | None,
    request_session: requests.Session | None,
    URL: str = BASE_URL,
) -> requests.Response | None:
    count_tries = 0
    response = None
    error = False
    while True:
        if count_tries > MAX_TRIES:
            error = True
            break
        try:
            if request_session is not None:
                response = request_session.get(URL)
            elif user is not None and page is not None:
                response = requests.get(URL % (user, page), headers=headers)
            else:
                response = requests.get(URL, headers=headers)
            break
        except ConnectionError:
            # print('break while', URL)
            logger.warn("break while " + URL)
            count_tries += 1
            sleep(0.5)
        except Exception:
            raise
    if error:
        print("Error while resolving url: ", URL)
        response = None
    return response


def parse_page_response(
    user: str | None,
    page: int | None,
    request_session: requests.Session | None,
    URL: str = BASE_URL,
) -> list | dict:
    response = try_request(
        user=user, page=page, request_session=request_session, URL=URL
    )
    if response is None:
        return {}
    if response.status_code == 200:
        return response.json() # type: ignore[no-any-return]
    else:
        print("Error", f"html status: {response.status_code}")
        raise Exception


def parse(user: str = DEFAULT_USER, URL: str = BASE_URL) -> dict:
    page = 1
    response = requests.get(URL % (user, page), headers=headers)
    if response.status_code != 200:
        print("Error", f"html status: {response.status_code}")
        return {}
    json: list = response.json()
    data: dict = {}
    while len(json) > 0 and page < 2:
        if isinstance(json, list):
            print(type(json))
            raise Exception
        new_data = get_data(json)
        data = merge_dicts(new_data, data)
        page += 1
        json = parse_page_response(
            user=user, page=page, URL=URL, request_session=None
        )

    return data


if __name__ == "__main__":
    result = parse()
    print(result)

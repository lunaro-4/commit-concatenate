import os
import pytest
import datetime
import requests
import requests.adapters
from django.conf import Path
from mock import MagicMock
from commit_concatenate import github_parcer

from commit_concatenate.github_parcer import (get_data,
                                              parse_commit_date,
                                              parse_page_response,
                                              parse_links_from_json,
                                              git_to_datetime,
                                              merge_dicts)

from tests.consts import (links_list, page_response)


from requests_testadapter import Resp

TEST_FILE_FOLDER = Path(__file__).resolve().parent
TEST_PAGE_URL = os.path.join(TEST_FILE_FOLDER, "page.json")
TEST_COMMIT_1_URL = os.path.join(TEST_FILE_FOLDER, "commit1.json")
TEST_COMMIT_2_URL = os.path.join(TEST_FILE_FOLDER, "commit2.json")


class LocalFileAdapter(requests.adapters.HTTPAdapter):
    def build_response_from_file(self, request):
        file_path = request.url[7:]
        with open(file_path, "rb") as file:
            buff = bytearray(os.path.getsize(file_path))
            file.readinto(buff)
            resp = Resp(buff)
            r = self.build_response(request, resp)

            return r

    def send(
        self,
        request,
        stream=False,
        timeout=None,
        verify=True,
        cert=None,
        proxies=None,
    ):
        return self.build_response_from_file(request)


@pytest.fixture(autouse=True)
def run_around_tests():
    requests_session = requests.session()
    requests_session.mount("file://", LocalFileAdapter())
    yield requests_session


# ------------ TESTS ------------- #


def test_parse_page(run_around_tests):
    response = parse_page_response(
        URL="file://" + TEST_PAGE_URL,
        request_session=run_around_tests,
        user=None,
        page=None,
    )

    assert response == page_response


def test_parse_links_from_json():
    parsed = parse_links_from_json(page_response)
    assert parsed == links_list


def test_parse_commit_date(run_around_tests):
    date_1 = parse_commit_date(
        URL="file://" + TEST_COMMIT_1_URL, requests_session=run_around_tests
    )
    date_2 = parse_commit_date(
        URL="file://" + TEST_COMMIT_2_URL, requests_session=run_around_tests
    )
    assert date_1 == "2024-05-26T21:18:51Z"
    assert date_2 == "2021-02-23T21:19:06Z"


def test_merge_data():
    date_1 = datetime.datetime.strptime("2024-12-05", "%Y-%m-%d").date()
    date_2 = datetime.datetime.strptime("2024-01-04", "%Y-%m-%d").date()
    date_3 = datetime.datetime.strptime("2024-02-01", "%Y-%m-%d").date()
    dict1: dict = {date_1: 1, date_2: 1}
    dict2: dict = {date_1: 1, date_3: 1}
    expect: dict = {date_1: 2, date_2: 1, date_3: 1}
    assert expect == merge_dicts(dict1, dict2)
    empty_dict: dict = {}
    assert dict2 == merge_dicts(dict2, empty_dict)
    assert dict2 == merge_dicts(empty_dict, dict2)

    pass


# def test_mock():
#     def return_one():
#         return 1
#     def return_two():
#         return 2
#     return_one = MagicMock(return_value=2)
#     assert return_one() == return_two()
def test_git_to_datetime():
    date_1 = "2024-05-26T21:18:51Z"
    date_2 = "2021-02-23T21:19:06Z"
    expect_date_1 = datetime.datetime.strptime("2024-05-26", "%Y-%m-%d").date()
    expect_date_2 = datetime.datetime.strptime("2021-02-23", "%Y-%m-%d").date()

    assert expect_date_1 == git_to_datetime(date_1)
    assert expect_date_2 == git_to_datetime(date_2)


def test_get_data(run_around_tests):
    links_to_test_commits = [
        "file://" + TEST_COMMIT_1_URL,
        "file://" + TEST_COMMIT_2_URL,
    ]
    github_parcer.parse_links_from_json = MagicMock(
        return_value=links_to_test_commits
    )
    data = get_data([{}], requests_session=run_around_tests)
    date_1 = datetime.datetime.strptime("2024-05-26", "%Y-%m-%d").date()
    date_2 = datetime.datetime.strptime("2021-02-23", "%Y-%m-%d").date()
    expected = {date_1: 1, date_2: 1}
    assert data == expected

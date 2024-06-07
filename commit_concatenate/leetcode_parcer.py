from datetime import date, datetime
import requests


#### returns data in dictionary of {datetime.date : number_of_commits}; size is tied to № of active days


DEFAULT_URL = "https://leetcode-api-faisalshohag.vercel.app/lunaro-4"


def parse(user: str = "lunaro-4") -> dict[date, int]:
    response = requests.get(
        "https://leetcode-api-faisalshohag.vercel.app/" + user
    )
    if response.status_code == 200:
        data = response.json()
        data = data["submissionCalendar"]
        data_keys = list(data.keys())
        datetime_data: dict = {}
        for i in data_keys:
            date = datetime.fromtimestamp(int(i))
            datetime_data[date.date()] = data.pop(i)
        return datetime_data
    else:
        print("Error", f"html status: {response.status_code}")
        return {}


if __name__ == "__main__":
    print(parse())

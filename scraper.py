import os
import gzip
import time
from datetime import datetime, timedelta
import requests
from retrying import retry
import tablib

HEADERS = {"Ocp-Apim-Subscription-Key": "18b56f8b0eda44efabe5d60a5270cc34"}

@retry(stop_max_attempt_number=5)
def get_response(url, params=None):
    """
    Hits the url and returns response, retries on on failure
    """
    seconds_per_request = 60 / 6
    time.sleep(seconds_per_request)
    if params:
        response = requests.get(
            url, params=params, headers=HEADERS, timeout=60, stream=False
        )
    else:
        response = requests.get(url, headers=HEADERS, timeout=60, stream=False)
    response.raise_for_status()
    return response

def daterange_gen(start_date, end_date):
    """
    Generates dates from start_date to end_date
    """
    date_range = []
    current_date = start_date
    while current_date <= end_date:
        date_range.append(current_date)
        current_date += timedelta(days=1)
    return date_range

def save_file(path, file):
    """
    Puts the response content into a dataset 
    and writes it to a csv file and gzips them
    """
    content = file.content.decode("utf-8")
    dataset = tablib.Dataset().load(content, format="csv")
    with gzip.open(path + ".gz", "wb") as f:
        f.write(dataset.export("csv").encode("utf-8"))
    print(f"{path} file saved successfully!")

def get_name(url, title):
    """
    fetches the name for the current report
    """
    data = get_response(url)
    for i in data.json()["items"]:
        if i["displayName"] == title:
            return i["name"]
    return None

def scrape(ip_list):
    requests.models.CONTENT_CHUNK_SIZE = 50 * 1024 * 1024
    for ip_dict in ip_list:
        name = get_name(ip_dict["url"], ip_dict["title"])
        csv_url = f"{ip_dict['url']}/{name}"
        params = ip_dict["params"]
        dates = ip_dict["dates"]
        start_date = datetime.strptime(dates["date_start"], "%m/%d/%Y").date()
        end_date = datetime.strptime(dates["date_end"], "%m/%d/%Y").date()
        date_range = daterange_gen(start_date, end_date)

        for date in date_range:
            params.update({dates["date_column"]: date.strftime("%Y-%m-%d")})
            response = get_response(csv_url, params=params)
            if response.status_code == 200:
                total_rows = int(response.headers["X-TotalRows"])
                directory_path = (
                        f"{ip_dict['title']}/{date.year}/{date.month}/{date.day}/"
                    )
                if total_rows > params["rowCount"]:
                    os.makedirs(directory_path, exist_ok=True)
                    part = 1
                    while params["startRow"] < total_rows:
                        save_file(f"{directory_path}{name}{part}.csv", response)
                        params["startRow"] += params["rowCount"]
                        response = get_response(csv_url, params=params)
                        part += 1
                    params["startRow"] = 1
                elif total_rows == 0:
                    print("skipping blank file")
                    continue
                else:
                    os.makedirs(directory_path, exist_ok=True)
                    save_file(f"{directory_path}{name}.csv", response)
            else:
                print(
                    "Failed to fetch data for file. Status code:", response.status_code
                )

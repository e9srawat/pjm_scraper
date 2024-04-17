import os
import gzip
import tablib
import time
import requests
from datetime import datetime, timedelta

HEADERS = {"Ocp-Apim-Subscription-Key": "18b56f8b0eda44efabe5d60a5270cc34"}

def save_file(path, file):
    content = file.content.decode('utf-8')
    dataset = tablib.Dataset().load(content, format='csv')
    with gzip.open(path + '.gz', "wb") as f:
        f.write(dataset.export('csv').encode('utf-8'))
    print(f"{path} file saved successfully!")
    
def timeout(timestamp):
    timestamp2 = time.mktime(time.localtime())
    diff = 60-(timestamp2 - timestamp)
    if diff > 0:
        print(f"Timeout reached waiting for {int(diff)} seconds")
        time.sleep(diff)
    return time.mktime(time.localtime())

def get_name(url, title):
    data = requests.get(url, headers=HEADERS, timeout=900, stream=False)
    for i in data.json()["items"]:
        if i["displayName"] == title:
            return i["name"]

def scrape(ip_list):
    requests.models.CONTENT_CHUNK_SIZE = 50 * 1024 * 1024
    for ip_dict in ip_list:
        name = get_name(ip_dict["url"],ip_dict["title"])
        csv_url = f"{ip_dict['url']}/{name}"
        params = ip_dict["params"]
        dates = ip_dict["dates"]
        start_date = datetime.strptime(dates["date_start"], "%m/%d/%Y").date()
        end_date = datetime.strptime(dates["date_end"], "%m/%d/%Y").date()
        date_range = []
        current_date = start_date
        while current_date <= end_date:
            date_range.append(current_date)
            current_date += timedelta(days=1)
        for date in date_range:
            params.update({dates["date_column"]: date.strftime("%Y-%m-%d")})
            year = date.year
            month = date.month
            day = date.day
            response = requests.get(
                csv_url, params=params, headers=HEADERS, timeout=900, stream=False
            )
            if response.status_code == 200: 
                if int(response.headers["X-TotalRows"]) > params["rowCount"]:
                    directory_path = f"{ip_dict['title']}/{year}/{month}/{day}/"
                    os.makedirs(directory_path, exist_ok=True)
                    part = 1
                    while params["startRow"] < int(response.headers["X-TotalRows"]):
                        save_file(f"{directory_path}{name}{part}.csv", response)
                        params["startRow"] += params["rowCount"]
                        response = requests.get(
                            csv_url, params=params, headers=HEADERS, timeout=900, stream=False
                        )
                        part += 1
                    params["startRow"] = 1
                elif int(response.headers["X-TotalRows"]) == 0:
                    print("skipping blank file")
                    continue
                else:
                    directory_path = f"{ip_dict['title']}/{year}/{month}/{day}/"
                    os.makedirs(directory_path, exist_ok=True)
                    save_file(f"{directory_path}{name}.csv", response)
            else:
                print(
                    f"Failed to fetch data for file. Status code:",
                    response.status_code,
                )

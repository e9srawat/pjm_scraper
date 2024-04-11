import os
import requests
from datetime import datetime, timedelta


def save_file(path, file):
    with open(path, "wb") as f:
        f.write(file.content)
    print(f"{path} file saved successfully!")


def scrape(ip_list):
    headers = {"Ocp-Apim-Subscription-Key": "18b56f8b0eda44efabe5d60a5270cc34"}
    title_map = {}
    for ip_dict in ip_list:
        if ip_dict["iso"] not in title_map:
            title_map[ip_dict["iso"]] = {}
            data = requests.get(ip_dict["url"], headers=headers, timeout=900)
            for i in data.json()["items"]:
                title_map[ip_dict["iso"]][i["displayName"]] = i["name"]
        name = title_map[ip_dict["iso"]][ip_dict["title"]]

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
            print(params)
            response = requests.get(
                csv_url, params=params, headers=headers, timeout=900
            )
            if response.status_code == 200:
                directory_path = f"{ip_dict['title']}/{year}/{month}/{day}/"
                os.makedirs(directory_path, exist_ok=True)
                if int(response.headers["X-TotalRows"]) > params["rowCount"]:
                    counter = 1
                    while params["startRow"] < int(response.headers["X-TotalRows"]):
                        save_file(f"{directory_path}{name}{counter}.csv", response)
                        params["startRow"] += params["rowCount"]
                        response = requests.get(
                            csv_url, params=params, headers=headers, timeout=900
                        )
                        counter += 1
                    params["startRow"] = 1
                else:
                    save_file(f"{directory_path}{name}.csv", response)
            else:
                print(
                    f"Failed to fetch data for file. Status code:",
                    response.status_code,
                )


scrape(
    [
        {
            "iso": "PJM",
            "url": "https://api.pjm.com/api/v1/",
            "title": "Day-Ahead Hourly LMPs",
            "params": {
                "rowCount": 1000000,
                "startRow": 1,
                "format": "csv",
                "download": True,
            },
            "dates": {
                "date_column": "datetime_beginning_ept",
                "date_start": "11/08/2022",
                "date_end": "11/10/2022",
            },
        },
    ]
)

import time
import requests


def scrape(ip_list):
    headers = {
        "Ocp-Apim-Subscription-Key": "18b56f8b0eda44efabe5d60a5270cc34",
    }
    title_map = {}
    for ip_dict in ip_list:
        if ip_dict["iso"] not in title_map:
            title_map[ip_dict["iso"]] = {}
            data = requests.get(ip_dict["url"], headers=headers, timeout=900)
            for i in data.json()["items"]:
                title_map[ip_dict["iso"]][i["displayName"]] = i["name"]

    timestamp = time.mktime(time.localtime())
    counter = 0
    for ip_dict in ip_list:
        name = title_map[ip_dict["iso"]][ip_dict["title"]]
        csv_url = f"{ip_dict['url']}/{name}"
        default_params = requests.get(csv_url, headers=headers, timeout=900)
        params = ip_dict["params"]
        if "filter" in ip_dict:
            for i in ip_dict["filter"]:
                params.update(i)
        else:
            for i in default_params.json()["searchSpecification"]["filters"]:
                params.update(i)
        response = requests.get(csv_url, params=params, headers=headers, timeout=900)
        if response.status_code == 200:
            with open(name + ".csv", "wb") as f:
                f.write(response.content)
            print(f"{name}.csv file saved successfully!")
        else:
            print(
                f"Failed to fetch data for {ip_dict['title']}. Status code:",
                response.status_code,
            )

        counter += 1
        if counter == 6:
            counter = 0
            diff = 60 - (time.mktime(time.localtime()) - timestamp)
            if diff > 0:
                time.sleep(diff)
            timestamp = time.mktime(time.localtime())


# scrape(
#         [
#             {
#             "iso":"PJM",
#             "url": "https://api.pjm.com/api/v1/",
#             "title":"Wind Generation",
#             "params":{"rowCount": 1000000,"startRow":1,'format': 'csv', 'download': True},
#             "filter":[{"datetime_beginning_ept":"01/26/2024 00:00 to 01/30/2024"}]
#             },
#             {
#             "iso":"PJM",
#             "url": "https://api.pjm.com/api/v1/",
#             "title":"Load Reconciliation Billing Determinants - Monthly",
#             "params":{"rowCount": 1000000,"startRow":1,'format': 'csv', 'download': True},
#             },
#             {
#             "iso":"PJM",
#             "url": "https://api.pjm.com/api/v1/",
#             "title":"Day-Ahead Marginal Value",
#             "params":{"rowCount": 1000000,"startRow":1,'format': 'csv', 'download': True},
#             "filter":[{"datetime_ending_ept":"Yesterday"}]
#             },
#             {
#             "iso":"PJM",
#             "url": "https://api.pjm.com/api/v1/",
#             "title":"Five Minute Load Forecast",
#             "params":{"rowCount": 1000000,"startRow":1,'format': 'csv', 'download': True},
#             "filter":[{"evaluated_at_ept":"Yesterday"}]
#             },
#             {
#             "iso":"PJM",
#             "url": "https://api.pjm.com/api/v1/",
#             "title":"Real-Time Ancillary Service Market Results",
#             "params":{"rowCount": 1000000,"startRow":1,'format': 'csv', 'download': True},
#             },
#             {
#             "iso":"PJM",
#             "url": "https://api.pjm.com/api/v1/",
#             "title":"Synchronized Reserve Events",
#             "params":{"rowCount": 1000000,"startRow":1,'format': 'csv', 'download': True},
#             },
#             {
#             "iso":"PJM",
#             "url": "https://api.pjm.com/api/v1/",
#             "title":"Regulation Prices",
#             "params":{"rowCount": 1000000,"startRow":1,'format': 'csv', 'download': True},
#             "filter":[{"datetime_beginning_ept":"Yesterday"}]
#             }
#         ]
#     )

import time
from bs4 import BeautifulSoup
import requests

def scrape(ip_list):
    url = 'https://api.pjm.com/api/v1/'
    headers = {
        'Ocp-Apim-Subscription-Key': '18b56f8b0eda44efabe5d60a5270cc34',
    }
    response_names = requests.get(url, headers=headers)

    t = time.localtime()
    timestamp = time.mktime(t)
    counter = 0
    for ip_dict in ip_list:
        for i in response_names.json()["items"]:
            if ip_dict["title"] == i["displayName"]:
                name = i["name"]

        csv_url = f"https://api.pjm.com/api/v1/{name}"
        param_data = requests.get(csv_url, headers=headers)

        fields = param_data.json()["searchSpecification"]["fields"]

        params = ip_dict["params"]
        # if "sort" in ip_dict and ip_dict["sort"] is not None:
        #     if ip_dict["sort"] not in fields:
        #         print(f"Invalid value for 'sort', available fields are: {', '.join(param_data.json()['searchSpecification']['fields'])}")
        #         return
        #     params["sort"] = ip_dict["sort"]

        # if "order" in ip_dict and ip_dict["order"] is not None:
        #     params["order"] = ip_dict["order"]

        # if "startRow" in ip_dict and ip_dict["startRow"] is not None:
        #     params["startRow"] = ip_dict["startRow"]

        # if "isActiveMetadata" in ip_dict and ip_dict["isActiveMetadata"] is not None:
        #     params["isActiveMetadata"] = ip_dict["isActiveMetadata"]

        # if "fields" in ip_dict and ip_dict["fields"] is not None:
        #     if not all([True if i in fields else False for i in ip_dict["fields"]]):
        #         print(f"Invalid values for fields, available fields are: {', '.join(param_data.json()['searchSpecification']['fields'])}") 
        #         return
        #     params["fields"] = ",".join(ip_dict["fields"])

        # if "datetime_ending_ept" in ip_dict :
        #     params['datetime_ending_ept'] = ip_dict["datetime_ending_ept"]

        # for i in param_data.json()["searchSpecification"]["filters"]:
        #         params.update(i)
        params['format']="csv"
        params['download']= True
        response = requests.get(csv_url, params=params, headers=headers)
        if response.status_code == 200:
            with open(name+".csv", "wb") as f:
                f.write(response.content)
            print(f"{name}.csv file saved successfully!")
        else:
            print(f"Failed to fetch data for {ip_dict['title']}. Status code:", response.status_code)

        counter += 1
        if counter==6:
            counter = 0 
            t2 = time.localtime()
            timestamp2 = time.mktime(t2)
            diff = 60-(timestamp2 - timestamp)
            print(diff)
            if diff > 0:
                time.sleep(diff)
            t = time.localtime()
            timestamp = time.mktime(t)


scrape(
        [
            {
            "title":"Wind Generation",
            "params":{"startRow":1,
            "datetime_beginning_ept":"Today"}
            },
            {
            "title":"Load Reconciliation Billing Determinants - Monthly",
            "params":{"startRow":1,
            "determinant_month":"Today"}
            },
            {
            "title":"Day-Ahead Marginal Value",
            "params":{"startRow":1,
            "datetime_ending_ept":"Today"}
            },
            {
            "title":"Five Minute Load Forecast",
            "params":{"startRow":1,
            "evaluated_at_ept":"Today"}
            },
            {
            "title":"Real-Time Ancillary Service Market Results",
            "params":{"startRow":1,
            "datetime_beginning_ept":"Today"}
            
            },
            {
            "title":"Synchronized Reserve Events",
            "params":{"startRow":1,
            "event_start_ept":"Today"}
            },
            {
            "title":"Regulation Prices",
            "params":{"startRow":1,
            "datetime_beginning_ept":"Today"}
            }
        ]
    )

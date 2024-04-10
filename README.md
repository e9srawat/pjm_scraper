

## PJM Scraper


The function ```scrape(ip_list):``` accepts a list of dictionaries as input, the dictionaries are the configurations for the report which has to be downloaded, the dictionary is in the format:

```python
{
    "iso": "PJM",
    "url": "https://api.pjm.com/api/v1/",
    "title": "Wind Generation",
    "params": {
        "rowCount": 1000000,
        "startRow": 1,
        "format": "csv",
        "download": True
    },
    "filter": [
        {
            "datetime_beginning_ept": "01/26/2024 00:00 to 01/30/2024"
        }
    ]
}
```
Here 
* iso is the iso name
* url is the url from where the data is to be fetched
* title is the name of the report to be downloaded
* params is the parameters to be passed
    * rowCount is the maximum number of rows that should be in the downloaded file 1000000 is the maximum limit any value above that will lead to a status code 400 error
    * startRow specifies the one-based number of the first record in the search results to be returned. This is one-based, so 1 is the smallest value allowed and will return the very first record
* Filter contains oarameters based on which the data should be filtered
    * Date Time Attributes are used to get the report for a specific time period

#### Following params can also be added
* sort: Specifies the name of the column to sort on
* order: Specifies the direction to sort the field on. Allowed values are: "asc" for ascending or "desc" for
descending order. The default value is "asc".
* fields: Specifies the name of the columns to be included in the file, by default all columns are included


#### Date Time Attributes can be entered in the following formats:
* Today (returns data for today's day) 
* Yesterday (returns data for today's date -1 day)
* LastWeek (returns data where the date falls within the last calendar week)
* LastMonth (returns data where the date falls within the last calendar month)
* CurrentMonth (returns data where the date value falls within the current month including current day)
* CurrentWeek (returns data where the date value falls within the current week including current day)
* CurrentYear (returns data where the date value falls within the current calendar year including current day)
* LastYear (returns data where the date value falls within the last calendar year)
* NextYear (returns data where the date value falls within the next calendar year)
* NextMonth (returns data where the date value falls within the next calendar month)
* NextWeek (returns data where the date value falls within the next calendar week)
* Tomorrow (returns data for current calendar day +1 day) 
* CurrentHour (returns data where the date value is equal to today’s date and the time is equal to the current hour)
* 1MonthAgo (returns data for the month where the date value falls within the current full calendar month minus one)
* 4MonthsAgo (returns data for the month where the date value falls within the current full calendar month minus four)
* 6MonthsAgo (returns data for the month where the date value falls within the current full calendar month minus six)
* LastHour (returns data where the date value is equal to today’s date and the time is equal to the current hour-1 hour)
* 15SecondsAgo (returns data where timestamp value is equal to current timestamp minus 15 seconds)
* 5MinutesAgo (returns data where timestamp value is equal to current timestamp minus 5 seconds)
* [date-value] to [date-value] The date-value should include the date and time component or the date component for applicable feeds. The date-value range should be within 366 days. Example: yyyy-mm-dd hh:mi to yyyy-mm-dd hh:mi

15SecondsAgo and 5MinutesAgo are designed specifically for dispatch rates and unverified LMP feeds
that update every 15 seconds and 5 minutes respectively, additionally these filters are designed to work
only with the ept columns, do not use with the utc columns.


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
    "dates": {
        "date_column":"datetime_beginning_ept", 
        "date_start":"11/08/2022", 
        "date_end":"11/10/2022"
    }
}
```
Here 
* iso is the iso name
* url is the url from where the data is to be fetched
* title is the name of the report to be downloaded
* params is the parameters to be passed
    * rowCount is the maximum number of rows that should be in the downloaded file 1000000 is the maximum limit any value above that will lead to a status code 400 error
    * startRow specifies the one-based number of the first record in the search results to be returned. This is one-based, so 1 is the smallest value allowed and will return the very first record
* Dates contains attributes related to date, the data will be downloaded only for the date range specified here, this attribute is mandatory
    * date_column: The column name from which the dates should be considered
    * date_start: The start date
    *date_end: The end date

#### Following params can also be added
* sort: Specifies the name of the column to sort on
* order: Specifies the direction to sort the field on. Allowed values are: "asc" for ascending or "desc" for
descending order. The default value is "asc".
* fields: Specifies the name of the columns to be included in the file, by default all columns are included
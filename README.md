# YFetcher

### **What does the application do?**

- Fetches the latest youtube videos for a predefined search query (cricket and football in this case; other search terms can also be added seamlessly) and stores the data in PostgreSQL and ElasticSearch. Videos are fetched every minute. All of this happens asynchronous. 
- Rolling of API keys is supported. If the quota for one key is exhausted, then the application will use the next available key for which the quota has been not exhausted. 
- An endpoint can be used for filtering and sorting. All of the responses are paginated.
  - filtering: Videos can be searched using their title and description. Partial matching is supported, thanks to Elastic Search
  - sorting: based on `published_at` attribute of the video.   


### Tech Used

DB: PostgreSQL, Elastic Search

API Server: Django, Django Rest Framework


### Instructions

- Navigation to the root of the project where docker-compose.yml file is present.
- Add data in the .env file

- run `docker-compose up -d`


### **Usage**

Start up the project (see instructions tab)

Use postman or curl to hit the following endpoint. By default, the results are sorted in descending order of  `published_at` field in `Video` model. By default, limit is set to 10 and offset to 0 (for pagination)

```
curl localhost:8000/feed/search/
```

**Output**

```json
{
    "count": 57,
    "next": "http://localhost:8000/feed/search/?limit=10&offset=10",
    "previous": null,
    "results": [
        {
            "title": "VASAI LIVE FINAL CRICKET",
            "unique_video_id": "LjVDN0beLnE",
            "description": "",
            "published_at": "2021-01-24T09:08:43Z",
            "thumbnail_url": "https://i.ytimg.com/vi/LjVDN0beLnE/default.jpg",
            "created_at": "2021-01-24T09:09:00.733238Z",
            "updated_at": "2021-01-24T09:09:00.733260Z"
        },
        {
            "title": "chiefofwaco&#39;s Live PS4 Broadcast",
            "unique_video_id": "rPjurIuVSgM",
            "description": "",
            "published_at": "2021-01-24T09:08:04Z",
            "thumbnail_url": "https://i.ytimg.com/vi/rPjurIuVSgM/default.jpg",
            "created_at": "2021-01-24T09:09:00.635049Z",
            "updated_at": "2021-01-24T09:09:00.635072Z"
        },
  		....
        ....
        ....
    ]
}
```



You can change the sort order by specifying it in the url

To sort in the ascending order of the published_at field

```
http://localhost:8000/feed/search/?sort=published_at
```



To sort in the descending order of the published_at field (if you don't specify `sort` param, this is the default)

```
http://localhost:8000/feed/search/?sort=-published_at
```



You can change the limit and offset (for pagination)

```
http://localhost:8000/feed/search/?limit=10&offset=10
```



Videos can be searched based on their title and description.

To search for the query term `cricket`

```
localhost:8000/feed/search/?q=cricket
```



Now you can combine all the following options to make complex queries

```
http://localhost:8000/feed/search/?q=cricket football&limit=10&offset=0&sort=-published_at
```

The following query 

- searches for videos that matches the term `cricket football` 
- sorts the results in the descending order of the published_at field and 
- returns the first 10 items.



You can easily add support for fetching videos for more search queries. Say, you want to also search youtube for 'basketball', then open `docker-compose.yml` replace 

`cd src && python manage.py fetchvideos cricket football` 

with

 `cd src && python manage.py fetchvideos cricket football basketball`

 in `backgroundworker` service.

All of the videos are fetched asynchronously. The non-asyncio code is run in a threadpool using [aiocrontab](https://github.com/bhaveshpraveen/aiocrontab) library (Shameless flex: I wrote this library while learning asyncio)



### Issues

- All the api keys might get exhaused. Solution is to add a new api key from a diff account.
- `web` service in docker-compose might restart multiple time initially. This is because by the time the container starts, ES is not ready to accept connections. This will gets fixed automatically. 
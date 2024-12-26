# atlys_assignment
Solution of first assignment given by  Atlys

NOTE: make sure redis is installed and running.

`pip install -r requirements.txt`

### then run the server using
`uvicorn app:app --reload`

### hit this below url
```https
POST http://127.0.0.1:8000/scrape?token=securetoken123
{
    "max_pages": 1
}
```

### sample response
```
{
    "scrapped": 24, # cache did not hit
    "unchanged": 0, # cache hit
    "status": "Scraping completed."
}
```

response we will store in **scraped_data.json** make sure and images will be downloaded in same location in `images` folder(must be present). 

import requests
import json

# HOST LIKE: 'http://localhost/'
ES_HOST = ''
ES_FIRST_SCROLL_URI = f'{ES_HOST}/index/_search?scroll=2m'
ES_SCROLL_URI = f'{ES_HOST}/_search/scroll'

file_list = []
count=0

# Query payload
payload = {
    'query': { 
        'match_all': {} 
    },
    "size": 1000
}

#Query first page
first_page_response = requests.post(ES_FIRST_SCROLL_URI, json=payload)

# Verify first response
try:
    r_json = first_page_response.json()
    scroll_id = r_json['_scroll_id']
    records = r_json['hits']['hits']
except KeyError:
    records = []
    scroll_id = None
    print(f'Error! Response: {first_page_response.json()}')

# While there are results, do logic and continue scrolling
while len(records) > 0:
    count += len(records)
    print(f'Parsing {len(records)} records...')
    ## DO LOGIC
    print(f'Total until now: {count}')
    
    # Continue scrolling
    scroll_payload = {
        'scroll': '2m',
        'scroll_id': scroll_id
    }
    scroll_response = requests.post(ES_SCROLL_URI, json=scroll_payload)

    try:
        r_json = scroll_response.json()
        scroll_id = r_json['_scroll_id']
        records = r_json['hits']['hits']
    except KeyError:
        records = []
        scroll_id = None
        print(f'Error! Response: {first_page_response.json()}')

    
print(f'Finished search with {len(file_list)} records found!')
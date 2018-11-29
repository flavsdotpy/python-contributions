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
scroll_payload = {
    'scroll': '2m'
}

# Response parser
def parse_response(r_json):
    # Returns empty if does not contain key '_scroll_id'
    scroll_id = r_json.get('_scroll_id', '')
    # Returns empty dict if does not contain key 'hits'
    # Eventually, if this happens, the next get method will return an empty list
    records = r_json.get('hits', {}).get('hits', [])
    return records, scroll_id

#Query first page
first_page_response = requests.post(ES_FIRST_SCROLL_URI, json=payload)

# Parse first response
records, scroll_id = parse_response(first_page_response.json())

# While there are results, do logic and continue scrolling
while len(records) > 0:
    count += len(records)
    print(f'Parsing {len(records)} records...')
    ## DO
    ## LOGIC
    ## HERE
    print(f'Total until now: {count}')
    
    # Continue scrolling if there is new page
    if scroll_id != '':
        scroll_payload['scroll_id'] = scroll_id
        scroll_response = requests.post(ES_SCROLL_URI, json=scroll_payload)
        records, scroll_id = parse_response(scroll_response.json())
    
print(f'Finished search with {len(file_list)} records found!')
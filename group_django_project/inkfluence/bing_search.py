import json
import requests

def read_bing_key():

    bing_api_key = None
    try:
        with open('bing.key','r') as f:
            bing_api_key = f.readline().strip()
    except:
        try:
            with open('../bing.key') as f:
                bing_api_key = f.readline().strip()
        except:
            raise IOError('bing.key file not found')

    if not bing_api_key:
        raise KeyError('Bing key not found')

    return bing_api_key

def read_custom_config():

    custom_config_id = None
    try:
        with open('custom_config.key','r') as f:
            custom_config_id = f.readline().strip()
    except:
        try:
            with open('../custom_config.key') as f:
                custom_config_id = f.readline().strip()
        except:
            raise IOError('custom_config.key file not found')

    if not custom_config_id:
        raise KeyError('Custom Config ID not found')

    return custom_config_id


def run_query(search_terms):
    bing_key = read_bing_key()
    customConfig = read_custom_config()
    search_url = 'https://api.bing.microsoft.com/v7.0/custom/search?'
    headers = {'Ocp-Apim-Subscription-Key': bing_key}
    params = {'q': search_terms, 'customConfig': customConfig, 'count': 6, 'textDecorations': True, 'textFormat': 'HTML'}

    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()

    results = []
    for result in search_results['webPages']['value']:
        results.append({
            'title': result['name'],
            'link': result['url'],
            'summary': result['snippet']})
    return results


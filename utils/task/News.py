import utils.nlp.numbers as numbers
import utils.logging as logging
import requests
import json

def parse_top(top: str):
    try: return int(top)
    except:
        try: return numbers.text_to_int(top)
        except Exception as e:
            logging.fail(e)
            return 5

with open('data/secrets.json', 'r') as f:
    api_key = json.load(f)['api_keys']['newsapi']
    f.close()

def main(top='5', category='all'):
    top = parse_top(top)
    url_params = {
    'apiKey': api_key,
    'sortBy': 'popularity',
    'q': category
    }
    main_url = " https://newsapi.org/v2/everything?"
    #print(url_params)
    if category != 'all':
        url_params['sortBy'] = 'publishedAt'
    res = requests.get(main_url, params=url_params)
    articles = res.json()
    status = articles['status']
    if status == 'error': 
        raise ValueError(f"""Error fetching news: "{articles['message']}" at "{articles['code']}".""")
    sources = []
    titles  = []
    content = []
    for article in range(top):
        if article < len(articles['articles']):
            sources.append(articles['articles'][article]['source']['name'])
            titles.append(articles['articles'][article]['title'])
            content.append(articles['articles'][article]['description'])
        else: break

    previous_element = None
    sources.reverse()
    for i in range(len(sources)):
        if sources[i] == previous_element:
            sources[i] = None
        else:
            previous_element = sources[i]
    sources.reverse()

    complete_text = []
    n=1
    for source, title, text in zip(sources, titles, content):
        complete_text.append(f'\n{n}. - '+title) #+':')
        #complete_text.append(text)
        if source != None: complete_text.append(' Provided by '+source+'.')
        n += 1

    return " ".join(complete_text)
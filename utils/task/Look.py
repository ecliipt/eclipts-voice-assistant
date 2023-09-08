import requests
from bs4 import BeautifulSoup

import utils.nlp.parse as parse

def main(place='here', _type_=None):
    if _type_ == None: raise ValueError('The type of place was not specified')

    place = parse.place_city(place)

    search_url = f"https://www.yelp.com/search/snippet?find_desc={_type_}&find_loc={place}&request_origin=user"
    search_response = requests.get(search_url)
    search_results = search_response.json()['searchPageProps']['mainContentComponentsListProps']

    results = []

    for result in search_results:
        if result['searchResultLayoutType'] == "iaResult":
            _name     = str(result['searchResultBusiness']['name'])
            _rating   = str(result['searchResultBusiness']['rating'])
            _location = result['searchResultBusiness']['neighborhoods'][0]
            results.append({'name': _name, 'rating': _rating, 'location': _location})

    if results == []: raise ValueError('Could not find any {_type_} places in {place}')
    results = sorted(results, key=lambda x: x['rating'], reverse=True)
    sentences = []
    for i in results:
        sentences.append(f"{i['name']}; located in {i['location']} street; with a {i['rating'].replace('.', ' point ')} star rating.")
    return " ".join(sentences)

if __name__ == '__main__':
    main(_type_='restaurant')
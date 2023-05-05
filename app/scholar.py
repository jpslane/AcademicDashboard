from googlesearch import search
import pickle


def load_data_from_cache():
    try:
        with open('scholar_cache.pickle', 'rb') as f:
            data = pickle.load(f)
    except FileNotFoundError:
        data = {}
    return data


def save_data_to_cache(data):
    with open('scholar_cache.pickle', 'wb') as f:
        pickle.dump(data, f)


def get_scholar(name):
    cache = load_data_from_cache()
    if name in cache:
        return cache[name]

    search_query = name + ' Google Scholar'
    url = None
    for r in search(search_query, num_results=2):
        if "scholar.google" in r and r != 'https://scholar.google.com/scholar':
            url = f'[{r}]({r})'
            break
    cache[name] = url
    save_data_to_cache(cache)
    return url

import requests
from bs4 import BeautifulSoup

url = 'https://quotes.toscrape.com'

url_for_links = url

def some_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "No more page."
        except IndexError:
            return "IE"
        except UnboundLocalError:
            return "ULE"
        except AttributeError:
            return "AE"
    return inner

@some_error
def swap_page(soup):
    next_page = soup.find('li', class_='next')
    if next_page:
        next_page = next_page.a['href']
        url = 'https://quotes.toscrape.com'+next_page
        next_page = None
        return url
    else:
        return None

@some_error
def  get_authors(soup):
    if soup:
        list = []
        authors  = soup.find_all('small', class_='author')
        for object in authors:
            list.append(object.text)
        return list

@some_error
def  get_quotes(soup):
    if soup:
        list = []
        qoutes = soup.find_all('span', class_='text')
        for object in qoutes:
            list.append(object.text)
        return list

@some_error
def  get_tags(soup):
    if soup:
        list = []
        tag_div = soup.find_all('div', class_='tags')
        for object in tag_div:
            tags = object.find_all('a', class_='tag')
            tags_list = []
            for object in tags:
                tags_list.append(object.text)
            list.append(tags_list)
        return list

@some_error
def make_qoutes(tags,author,quote):
    qoutes = []
    for i in range(len(author)):
        object = {}
        object['tags'] = tags[i]
        object['author'] = author[i]
        object['quote'] = quote[i]
        qoutes.append(object)
    return qoutes

@some_error
def  get_links(soup):
    if soup:
        list = []
        links = soup.find_all('a', href=True)
        for object in links:
            if '/author/' in object['href']:
                list.append(url_for_links+object['href'])
        return list

@some_error
def  get_fullname(soup):
    if soup:
        object  = soup.find('h3', class_='author-title')
        return object.text

@some_error
def  get_borndate(soup):
    if soup:
        object  = soup.find('span', class_='author-born-date')
        return object.text

@some_error
def  get_bornlocation(soup):
    if soup:
        object  = soup.find('span', class_='author-born-location')
        return object.text
    
@some_error
def  get_description(soup):
    if soup:
        object  = soup.find('div', class_='author-description')
        return object.text.strip()
    
@some_error
def make_author(fullname,borndate,bornlocation,description):
    object = {}
    object['fullname'] = fullname
    object['born_date'] = borndate
    object['born_location'] = bornlocation
    object['description'] = description
    return object

@some_error
def connect(url):
    if url:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
    return soup

@some_error
def main(url):
    links = []
    quotes = []
    authors = []
    while True:
        if url:
            soup = connect(url)
            links.extend(get_links(soup))
            quotes.extend(make_qoutes(get_tags(soup),get_authors(soup),get_quotes(soup)))
            url = swap_page(soup)
        else:
            for url in links:
                soup = connect(url)
                authors.append(make_author(get_fullname(soup),get_borndate(soup),get_bornlocation(soup),get_description(soup)))
            break
    return {'quotes': quotes, 'authors': authors}

if __name__ == "__main__":
    print(main(url))


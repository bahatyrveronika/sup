import requests
from bs4 import BeautifulSoup
import re
import sqlite3
import os
from urllib.parse import urlparse
import googlemaps


def create_database():
    conn = sqlite3.connect('/Users/veronikabagatyr-zaharcenko/Desktop/Flask web app tutoriall/website/restaurants.db')
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS restaurants
        (name TEXT, address TEXT, rating REAL, link TEXT, cuisine TEXT, tel TEXT, time TEXT, price REAL, image_path TEXT, child_room BOOLEAN DEFAULT FALSE,latitude REAL, longitude REAL)
    ''')

    conn.commit()
    return conn, c


def parse():
    conn, c = create_database()
    headers = {
        'authority': 'https://lasoon.net/ukr/lviv/vse-zavedeniya',
        'cache-control': 'max-age=0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Chrome/111.0.0.0',
        'sec-fetch-dest': 'document',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'accept-language': 'ua, ru; q=0.9'
    }
    restaurants = {}
    session = requests.session()
    k = 0
    resp = session.get('https://lasoon.net/ukr/lviv/vse-zavedeniya/1', headers=headers)
    if resp.status_code != 200:
        raise ValueError('Not connecting')

    k = 1
    while resp.status_code == 200:
        resp = session.get(f'https://lasoon.net/ukr/lviv/vse-zavedeniya/{k}', headers=headers)
        soup = BeautifulSoup(resp.text, 'html.parser')
        for item in soup.find_all('div', class_='b-right'):
            name = item.find('span', itemprop="name").text
            address = item.find('span', itemprop="address")
            if address is not None:
                address = address.text
            else:
                address = 'No address'
            print(name)
            print(address)
            rating = item.find('span', class_='rating1__title rating__value rating__value--custom')
            if rating is not None:
                rating = float(rating.text)
            else:
                rating = 'No rate'
            print(rating)
            link = 'https://lasoon.net' + item.find('h2', class_='mauto').find('a').get('href')
            res_resp = session.get(link, headers=headers)
            if res_resp.status_code != 200:
                raise ValueError('Not connecting')
            res_soup = BeautifulSoup(res_resp.text, 'html.parser')

            cuisine = res_soup.find('span', class_='span-line span-line-2')
            if cuisine is not None:
                cuisine = cuisine.text.replace('\n', '')
            else:
                cuisine = 'No cuisine'

            tel = res_soup.find('span', class_='rest tel')
            if tel is not None:
                tel = tel.find('a').get('href').replace('tel:', '')
            else:
                tel = 'No tel'

            time = res_soup.find('span', class_='rest rest_work')
            if time is not None:
                time = time.text
            else:
                time = 'No time'
            print(time)

            print(cuisine)
            print(tel)
            price=res_soup.find('span', itemprop="priceRange")
            if price is not None:
                price=price.text
                if '<' in price:
                    price=price.replace(' ₴','').replace('<','')
                else:
                    price=price.replace(' ₴','').split(' – ')
                    price = (int(price[0]) + int(price[1]))/2
            else:
                price='No price'

            child_room=False
            if 'Дитяча гральна кімната' in res_resp.text or 'Дитячий майданчик' in res_resp.text or 'Дитячий куточок' in res_resp.text:
                child_room=True

            def save_image(image_url, save_directory, folder_name):
                response = requests.get(image_url, stream=True)
                response.raise_for_status()
                parsed_url = urlparse(image_url)
                image_name = os.path.basename(parsed_url.path)
                os.makedirs(save_directory, exist_ok=True)
                invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
                for char in invalid_chars:
                    folder_name = folder_name.replace(char, '')
                restaurant_directory = os.path.join(save_directory, folder_name)
                os.makedirs(restaurant_directory, exist_ok=True)
                image_path = os.path.join(restaurant_directory, image_name)
                with open(image_path, 'wb') as image_file:
                    for chunk in response.iter_content(chunk_size=8192):
                        image_file.write(chunk)

                return image_path
            images = res_soup.find_all('img')
            im_list = []
            for image in images:
                img_name = image['alt']
                link_img = image['src']
                link_img = 'https://lasoon.net' + link_img
                if 'width' in image.attrs:
                    width = int(image['width'].replace('px', ''))
                else:
                    width = 0
                # width = int(image['width'].replace('px', ''))
                if 'height' in image.attrs:
                    height = int(image['height'].replace('px', ''))
                else:
                    height = 0
                if width >= 800 and height >= 400 and 'jpg'in link_img:
                    im_list.append(link_img)
                    image_url = link_img
                    save_directory = "static/photo"
                    image_path = save_image(image_url, save_directory, name)
                if len(im_list) == 4:
                    break

            def coordinates_find(adress):
                api_key = 'AIzaSyBfZU8rUJWOZxsgbBp1DXzgDKQs0_0bHF4'
                gmaps = googlemaps.Client(key=api_key)
                try:
                    geocode_result1 = gmaps.geocode(adress)
                    if geocode_result1:
                        location = geocode_result1[0]['geometry']['location']
                        latitude = location['lat']
                        longitude = location['lng']
                        coordinates = [latitude, longitude]
                        return coordinates
                    else:
                        print("Could not find coordinates for the address.")
                        return None
                except Exception as e:
                    print("Error:", e)
                    return None
            coordinates = coordinates_find(address)
            if coordinates is not None:
                latitude = coordinates[0]
                longitude = coordinates[1]
            else:
                latitude = 'No latitude'
                longitude = 'No longitude'



            c.execute('''
                INSERT INTO restaurants (name, address, rating, link, cuisine, tel, time, price, image_path, child_room,  latitude, longitude)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (name, address, rating, link, cuisine, tel, time, price, image_path, child_room,  latitude, longitude))

            conn.commit()
        k += 1
    conn.close()


parse()

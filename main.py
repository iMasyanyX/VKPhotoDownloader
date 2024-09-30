import os
import requests
import time

# Ваш токен доступа (можно получить через VK API)
ACCESS_TOKEN = 'token'
# ID сообщества без "club" или "public", например 123456789
GROUP_ID = 'id'
# Версия API
API_VERSION = '5.131'


# Функция для получения списка альбомов
def get_albums(group_id):
    url = 'https://api.vk.com/method/photos.getAlbums'
    params = {
        'access_token': ACCESS_TOKEN,
        'v': API_VERSION,
        'owner_id': f'-{group_id}',  # для групп необходимо передавать ID с минусом
        'need_system': 1,
        'photo_sizes': 1
    }
    response = requests.get(url, params=params).json()
    return response['response']['items']


# Функция для получения фотографий из альбома
def get_photos_from_album(album_id, group_id):
    url = 'https://api.vk.com/method/photos.get'
    params = {
        'access_token': ACCESS_TOKEN,
        'v': API_VERSION,
        'owner_id': f'-{group_id}',
        'album_id': album_id,
        'photo_sizes': 1
    }
    response = requests.get(url, params=params).json()
    return response['response']['items']


# Функция для скачивания фотографий
def download_photo(url, dest_folder, filename):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    response = requests.get(url)
    with open(os.path.join(dest_folder, filename), 'wb') as f:
        f.write(response.content)


# Основная функция для скачивания всех альбомов
def download_albums(group_id):
    albums = get_albums(group_id)

    for album in albums:
        album_title = album['title'].replace('/', '_')  # Убираем нежелательные символы для названий папок
        album_id = album['id']

        print(f"Скачивание альбома: {album_title} (ID: {album_id})")

        # Папка для альбома
        album_folder = os.path.join('vk_photos', album_title)

        photos = get_photos_from_album(album_id, group_id)

        for i, photo in enumerate(photos):
            # Получаем URL самого большого изображения
            sizes = photo['sizes']
            largest_photo = max(sizes, key=lambda size: size['width'] * size['height'])
            photo_url = largest_photo['url']
            photo_id = photo['id']

            # Формируем имя файла
            filename = f"{photo_id}.jpg"

            # Скачиваем фото
            download_photo(photo_url, album_folder, filename)
            print(f"Скачано: {filename}")


if __name__ == "__main__":
    download_albums(GROUP_ID)

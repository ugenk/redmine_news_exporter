import requests, os
from xml.etree import ElementTree


def get_news(url, limit, api_key, delim):
    offset = 0
    headers = {'X-Redmine-API-Key': api_key}  # Заголовок для передачи ключа API

    while True:
        response = requests.get(url, headers=headers, params={'limit': limit, 'offset': offset})
        response.raise_for_status()  # Проверяем, что запрос был успешным
        content = response.content

        # Разбираем XML
        root = ElementTree.fromstring(content)
        # Проверяем наличие элементов новостей
        news_items = root.findall('.//news')

        if not news_items:
            # Если больше нет элементов новости, прерываем цикл
            break
        
        # Обработка новостей
        for item in news_items:
            # Здесь вы можете извлечь и обработать информацию о каждой новости
            # Например, мы можем вывести заголовок и ссылку каждой новости
            author = item.find('author').get("name")
            title = item.find('title').text
            description = item.find('description').text.replace('\n', ' ')
            created_on = item.find('created_on').text
            print(f"\'{author}\'{delim}\'{created_on}\'{delim}\'{title}\'{delim}\'{description}\'")
        
        # Увеличиваем смещение для следующего запроса
        offset += limit


# Начальная точка
base_url = os.environ.get('REDMIME_NEWS_URL', '')
limit = 100  # Можно настроить в соответствии с ограничениями API
api_key = os.environ.get('REDMINE_API_KEY', '')
delimiter = '^'  # CSV-разделитель полей

# Запускаем функцию для получения всех новостей
get_news(base_url, limit, api_key, delim=delimiter)

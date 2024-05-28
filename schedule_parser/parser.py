import re
import shutil
import os


import asyncio
import aiohttp
from aiohttp import ClientSession
from bs4 import BeautifulSoup

from schedule_parser.execution_function import calculate_execution_time
from common import ROOT_DIR


async def del_all_data() -> None:
    """
    Удаляет все файлы из папки {ROOT_DIR}/schedule
    :return: None
    """
    folder_path = f"{ROOT_DIR}/schedule"  # Путь к папке с расписанием

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


@calculate_execution_time
async def parse_data() -> None:
    """
    Главная функция парсера сайта расписаний КФУ.
    :return: None
    """
    await del_all_data()
    # URL страницы для парсинга
    url = "https://cfuv.ru/raspisanie-uchebnykh-zanyatijj"
    # Отправляем GET-запрос и получаем содержимое страницы
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            content = await response.content.read()

    # Создаем объект BeautifulSoup для парсинга HTML
    soup = BeautifulSoup(content, "html.parser")

    # Находим все строки таблицы, содержащие "(структурное подразделение)"
    links = []
    for link in soup.find_all('p'):
        for a in link:
            if 'https://cfuv.ru/raspisanie' in str(a):
                links.append(a.get('href'))
                break

    links.pop(0)
    print(links)
    # Добавляем то что почему-то не спрасилось
    links.append('https://cfuv.ru/institut-mediakommunikacijj-mediatekhnologijj-i-dizajjna')
    links.append('https://cfuv.ru/raspisanie-fakultativov-akademiyai-bioresursov-i-prirodopolzovaniya')

    sub_links = {}
    sub_links_bad = {}

    try:
        # Добавляем так же файлы с группами ДУК и ЦК
        for link in soup.find_all('a'):
            if "(цифровая подготовка)" in link.text:
                sub_links[link['href']] = 'ЦК'
            if "дисциплин универсальных компетенций" in link.text.lower():
                sub_links[link['href']] = 'ДУК'
    except:
        print('ЦК НЕ НАШЕЛ')

    for link in links:
        url = str(link)
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        content = await response.content.read()
                        soup = BeautifulSoup(content, 'html.parser')
                        # Поиск всех ссылок с href, содержащим 'https://schedule-cloud.cfuv.ru/'
                        print(f'Рассматриваю: {link}')
                        for a in soup.find_all('a', href=re.compile('https://schedule-cloud.cfuv.ru/')):
                            href = a['href']
                            text = a.get_text(strip=True)
                            # Эти ссылки мы отбрасываем в другую кучу из-за того что их надо дополнительно обработать
                            if url != 'https://cfuv.ru/raspisanie-fakultativov-akademiyai-bioresursov-i-prirodopolzovaniya' and url != 'https://cfuv.ru/raspisanie-akademii-stroitelstva-i-arkhitektury':
                                sub_links[href] = text
                            else:
                                sub_links_bad[href] = text
                        print('УСПЕШНО')
        except aiohttp.ClientError as ex:
            print("Ошибка при проверке доступности сайта:", ex)
    print(sub_links)
    for el, el2 in sub_links.items():
        print(f'{el}, {el2}')

    # папка для сохранения файлов
    save_folder = f"{ROOT_DIR}/schedule"

    # проверка существования папки
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    # перебор всех ссылок и скачивание файлов асинхронно
    tasks = []
    async with aiohttp.ClientSession() as session:
        for url, filename in sub_links.items():
            tasks.append(download_file(session, url, filename, f'{ROOT_DIR}/schedule'))

        for url, filename in sub_links_bad.items():
            tasks.append(download_file(session, url, filename, f'{ROOT_DIR}/schedule/need_handle'))

        await asyncio.gather(*tasks)


async def download_file(session: ClientSession, url: str, filename: str, folder: str) -> None:
    """
    Качает файлы .xls, .xlsx, .doc, .docx в папку {ROOT_DIR}/schedule
    :param session: Сессия скачивания
    :param url: Ссылка для скачивания
    :param filename: Имя скачиваемого файла
    :param folder: Папка для сохранения файлов
    :return: None
    """
    async with session.get(url) as response:
        if response.status == 200:
            content = await response.content.read()
            soup = BeautifulSoup(content, 'html.parser')
            link_div = soup.find('div', class_="directDownload")
            download_url = link_div.find('a')['href']
            if download_url.endswith(".docx") or download_url.endswith(".doc"):
                return
            file_name = link_div.find('div').get_text(strip=True)
            file_name = file_name.split('\xa0')[0]
            file_content = await download_file_content(session, download_url)
            if not os.path.exists(folder):
                os.makedirs(folder)
            with open(f'{folder}/{file_name}', 'wb') as f:
                f.write(file_content)


async def download_file_content(session: ClientSession, url: str) -> bytes | None:
    """
    Собственно сама качающая хрень.
    :param session: Сессия клиента.
    :param url: Ссылка.
    :return: Скачивает файл в папку, либо ошибка.
    """
    async with session.get(url) as response:
        if response.status == 200:
            return await response.content.read()
        else:
            print(f'Ошибка скачивания файла по ссылке {url}')
            return

if __name__ == "__main__":
    asyncio.run(parse_data())

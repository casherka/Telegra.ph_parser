from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import requests
import os
import datetime
from proxy_settings import proxy
from proxy_settings import use_proxy

style = '''<style>
    div header h1 {
        font-family: CustomSansSerif, 'Lucida Grande', Arial, sans-serif;
        font-weight: 700;
        font-style: normal;
        font-size: 32px;
        margin: 21px 21px 12px;
        line-height: 34px;
        color: rgba(0, 0, 0, .8);
    }

    @media (max-width: 1365px) {
    div header h1 {
        font-family: CustomSansSerif, 'Lucida Grande', Arial, sans-serif;
        font-weight: 700;
        font-style: normal;
        font-size: 24px;
        margin: 21px 21px 12px;
        line-height: 34px;
        color: rgba(0, 0, 0, .8);
    }}

    div header address {
        font-family: CustomSansSerif, 'Lucida Grande', Arial, sans-serif;
        font-size: 15px;
        line-height: 18px;
        color: #79828B;
        margin: 12px 21px;
        font-style: normal;
    }

    @media (max-width: 1365px) {
    div header address {
        font-family: CustomSansSerif, 'Lucida Grande', Arial, sans-serif;
        font-size: 12px;
        line-height: 18px;
        color: #79828B;
        margin: 12px 21px;
        font-style: normal;
    }}

    div p {
        margin: 0 21px 12px;
        word-wrap: break-word;
        font-family: CustomSerif, Georgia, Cambria, 'Times New Roman', serif;
        font-weight: 400;
        font-style: normal;
        font-size: 18px;
        line-height: 1.58;
        padding: 0;
        color: rgba(0, 0, 0, .8);
    }
    
    div {
        max-width: 732px;
        margin: 0 auto;
        position: relative;
        padding: 21px 0;
        width: 100%;
        flex-grow: 1;
    }

    @media (max-width: 1365px) {
    div p {
        margin: 0 21px 12px;
        word-wrap: break-word;
        font-family: CustomSerif, Georgia, Cambria, 'Times New Roman', serif;
        font-weight: 400;
        font-style: normal;
        font-size: 18px;
        line-height: 1.58;
        padding: 0;
        color: rgba(0, 0, 0, .8);
        width:77%;
    }}

    @media (max-width: 1365px) {
    div {
        max-width: 732px;
        margin: 0 20px;
        position: relative;
        padding: 21px 0;
        width: 100%;
        flex-grow: 1;
    }}

    div aside a {
        position: fixed;
        left: 47.2%;
        top: 75px;
        margin: 46px 0 0 376px;
        font-family: CustomSansSerif, 'Lucida Grande', Arial, sans-serif;
        font-weight: 600;
        font-style: normal;
        font-size: 17px;
        color: #000;
        text-align: center;
        text-transform: uppercase;
        padding: 0 0;
        cursor: pointer;
        width: 350px;
        text-decoration: unset;
        background-color: #ffffff00;
    }

    @media (max-width: 1365px){
    div aside a {
        position: fixed;
        left: 23%;
        top: 75px;
        right: 0;
        margin: 46px 0 0 376px;
        font-family: CustomSansSerif, 'Lucida Grande', Arial, sans-serif;
        font-weight: 600;
        font-style: normal;
        font-size: 17px;
        color: #000;
        text-align: center;
        text-transform: uppercase;
        padding: 0 0;
        cursor: pointer;
        width: 350px;
        text-decoration: unset;
        background-color: #ffffff00;
    }}
    
    div header address a {
        margin-right: 12px;
    }
</style>'''

proxies_set = {
  "http": proxy,
  "https": proxy
}

color_table = {'Blue': '\033[94m',
               'Green': '\033[92m',
               'Red': '\033[91m',
               'Purple': '\033[95m',
               'Mark': '\033[100m',
               'Clear': '\033[0m'}


class CreateFolder:
    folder_name = "folder_title date_time"

    def __init__(self, folder_title, folder_datetime):

        self.folder_name = f"{folder_title} {folder_datetime.replace(':', ';')}"

        try:
            os.mkdir(self.folder_name)
        except FileExistsError:
            pass


def datetime_calculate():
    start_datetime_ms = str(datetime.datetime.now())
    start_datetime = start_datetime_ms[:start_datetime_ms.find('.')] if '.' in start_datetime_ms else start_datetime_ms

    return start_datetime


def send_request(title, month, day,  folder_path, using_proxy: bool = False):
    headers = {"User-Agent": UserAgent().random, "Accept": "text/html"}

    if using_proxy:
        request = requests.get(f'https://telegra.ph/{title}-{month}-{day}', headers, proxies=proxies_set)
    else:
        request = requests.get(f'https://telegra.ph/{title}-{month}-{day}', headers)

    request_text = request.text
    soup = BeautifulSoup(request_text, 'html.parser')

    if request.status_code == 200:
        with open(f"{folder_path}/{title}-{month}-{day}.html", "w", encoding='utf-8') as file:
            file.write('<div>' + str(soup.header) +
                       F"{''.join(map(str, soup.article.find_all('p')))}"
                       F"<aside><a href='https://telegra.ph/{title}-{month}-{day}'>"
                       F"|Online| https://telegra.ph/{title}-{month}-{day}</a></aside>"
                       F"</div>\n" + style)

            print(f"{color_table['Mark']}{color_table['Green']}File_saved {title}-{month}-{day}.html")
    elif request.status_code == 404:
        print(f"{color_table['Clear']}{color_table['Red']}N/a {title}-{month}-{day}")


def main():
    date_time = datetime_calculate()

    print(f"{color_table['Clear']}{color_table['Purple']}Start date and time: {date_time}")

    parse_title = input(f"{color_table['Clear']}{color_table['Blue']}Title: ").capitalize()

    folder_name = CreateFolder(parse_title, date_time).folder_name

    for i in range(1, 13):
        month = str(i)
        if len(month) == 1:
            month = '0' + str(i)
        for k in range(1, 32):
            day = str(k)
            if len(day) == 1:
                day = '0' + str(k)
            send_request(parse_title, month, day, folder_name, use_proxy)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"{color_table['Clear']}{color_table['Purple']}Exit")

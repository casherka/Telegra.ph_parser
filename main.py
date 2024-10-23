from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import requests
import os
import datetime
from Settings.proxy_settings import proxy
from Settings.proxy_settings import use_proxy
from OfflineVersion.styles import style
from Settings import color_scheme

proxies_set = {
  "http": proxy,
  "https": proxy
}

color_dict = {'Blue': color_scheme.Blue,
              'Green': color_scheme.Green,
              'Red': color_scheme.Red,
              'Purple': color_scheme.Purple,
              'Mark': color_scheme.Mark,
              'Clear': color_scheme.Clear
              }


class CreateFolder:
    folder_name = "folder_title date_time"

    def __init__(self, folder_title, folder_datetime):

        self.folder_name = f"{folder_title} {folder_datetime.replace(':', ';')}"

        try:
            os.mkdir(self.folder_name)
        except FileExistsError:
            pass


def t_parser_print():
    print(f"{color_dict['Clear']}{color_dict['Green']}")
    print("  ___________________________________________"
          "____________________________________________________________")
    print("  |   **********    ********      ***        "
          "    ********        *******         ********     ********  |")
    print("  |      **        **    **     **  **      "
          "    **      **      **     **       ********     **      ** |")
    print("  |     **        ********    **     **     "
          "   **       **     **              **           **     **   |")
    print("  |    **        **          **********    "
          "   **********      **********      ********     **********   |")
    print("  |   **        **          ***********   "
          "   **  **                  **      **           **  **        |")
    print("  |  **        **          **        **  "
          "   **    **        **      **      ********     **    **       |")
    print("  | **        **          **         **  "
          "  **      **        ********      ********     **      **      |")
    print("  ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯"
          "¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯")
    print(color_dict['Clear'])


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
            file.write('<div>' + str(soup) +
                       F"<aside><a href='https://telegra.ph/{title}-{month}-{day}'>"
                       F"|Online| https://telegra.ph/{title}-{month}-{day}</a></aside>"
                       F"</div>\n" + style)

            print(f"{color_dict['Mark']}{color_dict['Green']}File_saved {title}-{month}-{day}.html")
    elif request.status_code == 404:
        print(f"{color_dict['Clear']}{color_dict['Red']}N/a {title}-{month}-{day}")


def main():
    date_time = datetime_calculate()

    print(f"{color_dict['Clear']}{color_dict['Purple']}Start date and time: {date_time}")

    parse_title = input(f"{color_dict['Clear']}{color_dict['Blue']}Title: ").capitalize()

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
        t_parser_print()
        main()
    except KeyboardInterrupt:
        print(f"{color_dict['Clear']}{color_dict['Purple']}Exit")

import requests
from bs4 import BeautifulSoup, NavigableString, Tag


class IlMeteo:
    base_url = "https://www.ilmeteo.it/portale/meteo/previsioni1.php?c="

    @staticmethod
    def get_id():
        f1 = open('ilmeteo', 'w')
        for x in range(0, 8986):
            url = IlMeteo.base_url + str(x) + "&gm=7&g=0"
            request = requests.get(url)
            html_data = request.text
            parsed_html = BeautifulSoup(html_data, "html.parser")
            title = parsed_html.title.string
            finalindex = title.find("-") - 1
            city = title[24:finalindex]
            f1.write(str(x) + "," + city.encode('utf-8') + "\n")
            print (str(x) + "," + city.encode('utf-8') + "\n")
        f1.close()

IlMeteo.get_id()
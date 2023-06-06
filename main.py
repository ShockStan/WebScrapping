from bs4 import BeautifulSoup
import pandas as pd
import requests


def collectData(url):
    html_data = requests.get(url)
    soup = BeautifulSoup(html_data.content, 'lxml')
    table_body = soup.find('tbody')
    table_rows = table_body.find_all('tr')
    result = []
    for row in table_rows:
        table_data = row.find_all('td')
        data_list = []
        index = 1
        for data in table_data:
            if index == 4:
                price = data.find('p').text
                data_list.append(price)
            elif index == 3:
                name = data.find('p').text
                shortform = data.find_all('span')[-1].text
                data_list.append(name)
                data_list.append(shortform)
            else:
                data_list.append(data.text)
            index += 1
        for i in range(2):
            data_list.pop()
            del data_list[0]
        result.append(data_list)
    return result


if __name__ == '__main__':
    array = []
    for i in range(1, 348):
        url = f'https://crypto.com/price?page={i}'
        array.append(collectData(url))
        print(i)
    result = [item for sublist in array for item in sublist]
    headers = ['Name','Shortform','Price','24H change','24H volume', 'Market Cap']
    df = pd.DataFrame(result, columns=headers)
    df.to_json('result.json')


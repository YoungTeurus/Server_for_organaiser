import requests

if __name__ == "__main__":
    url = 'http://localhost:80'
    # payload = {
    #    'username': 'user1',
    #    'password': 'qwertyk'
    # }
    # files = {'file': ('test.txt', open('test.txt','rb'), 'text/txt')}
    # b = requests.get('http://localhost:80', data=payload, files=files)
    # print(b.url)
    # print(b.text)

    # Загрузка файла с сервера
    my_req = requests.get(url)
    file = open("mydata.json", "wb")
    file.write(my_req.content)
    file.close()

    # Отправка файла на сервер
    files = {'file': ('mydata3.json', open("mydata.json", "rb"), 'text/json')}
    try:
        my_req2 = requests.post(url, files=files)
    except requests.exceptions.ConnectionError:
        print("Бяка")

import requests


def translate(text, lang, language):
    """" Обращение к API Яндекс преводчика для перевода """
    URL = "https://translate.yandex.net/api/v1.5/tr.json/translate"  # куда отправляем запрос
    KEY = "trnsl.1.1.20200526T072738Z.e1dca6cc842663f6.37a8927e88ca396cb67ffbc65118b1d596982065"  # ключ полученный на сайте яндекса
    la = str(language + '-{}')  # переменная которая подменяет язык с которого надо перевести в отправляемых запросах

    params = {
        'key': KEY,
        'text': text,
        'lang': la.format(lang),  # параметры которые отправляются в запросе
    }

    response = requests.get(URL, params=params)  # отправляем запрос на url  и с заданными парамтрами
    json_ = response.json()  # полученный результат преобразуем в json
    print("Перевод: " + ''.join(json_['text']))
    return ''.join(json_['text'])  # преобразуем результат из списка в строку и возвращаем


def main(text, lang, language):  # приянли все 3 параметра
    print("Текст для перевода: " + text)
    name_files = "Translated document " + language.upper() + ".txt"  # создали имя создаваемого документа
    with open(name_files, "w", encoding="utf-8") as f:  # открыли или создали файл для записи результата, указали параметр для ДОзаписи и кодировку и записали все это в переменную f
        f.write(translate(text, lang, language))  # Передаем в функцию 3 параметра. Полученный результат записываем в переменную f


def download(name_files):
    """ Загрузка файлов на диск """
    URL = "https://cloud-api.yandex.net/v1/disk/resources/upload"  #
    path = "/" + name_files  # путь куда на ЯД загрузить(корень)
    token = "OAuth AgAEA7qizIRBAADLW4R9aNCSREMag6JLwmvzj6A"

    # Получаем ссылку для загрузки файла
    params = {"path": path, 'overwrite': 'true'}
    headers = {'Accept': 'application/json', "Authorization": token}
    res = requests.get(URL, params=params, headers=headers)
    # json_ = res.json()
    URL_DOWNLOAD = res.json().get('href')
    print("Ссылка для загрузки: " + URL_DOWNLOAD)

    # Загружаем файл на диск
    path_computer = 'D:\progs\\telegram\\' + name_files  # путь где лежит файл на компьютере
    file = {"file": open(path_computer, "rb")}
    res_download = requests.put(URL_DOWNLOAD, files=file)
    print(res_download)
    print(type(res_download))


if __name__ == "__main__":
    docs = {"DE.txt": "de", "ES.txt": "es", "FR.txt": "fr"}  # словарь с файлами и языком на который перевести надо
    for doc, language in docs.items():  # прогоняем каждый документ на перевод
        main(open(doc, encoding='utf-8').read(), "ru", language)  # отправляем с 3 параметрами(названием документа из словаря, язык на который перевести надо, и язык в файле)

    for doc in docs:
        name_files = "Translated document " + doc  # создали имя создаваемого документа
        download(name_files)


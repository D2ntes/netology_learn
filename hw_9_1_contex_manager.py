from time import localtime, time, asctime


class timer():
    def __init__(self, label):
        self.label = label

    def __enter__(self):
        self.start = time()
        print('Начало выполнения: ', asctime(localtime(self.start)))

    def __exit__(self, exc_ty, exc_val, exc_tb):
        end = time()
        print('Окончание выполнения: ', asctime(localtime(end)))
        print(self.label, end - self.start, 'сек.\n')


def create_list_generator(max_number):
    print('Создание списка с помощью генератора')
    return [i ** 3 for i in range(max_number)]


def create_list_for(max_number):
    print('Создание списка с помощью цикла и метода append')
    list_new = []
    for i in range(max_number):
        list_new.append(i ** 3)
    return list_new


count_number = 10000000

with timer('Время выполнения: '):
    import xml.etree.ElementTree as ET

    tree = ET.parse("newsafr.xml")
    root = tree.getroot()
    xml_items = root.findall("channel/item/description")
    words = []
    for xmli in xml_items:
        for word in (xmli.text.lower().split()):
            if len(word) > 6:
                words.append(word)

    # words_len = (list(filter(lambda x: len(x) > 6, words)))
    print(*sorted(set(words), key=lambda word: (-words.count(word), word))[:10], sep='\n')

with timer('Время выполнения: '):
    # import xml.etree.ElementTree as ET

    tree = ET.parse("newsafr.xml")
    root = tree.getroot()
    xml_items = root.findall("channel/item/description")
    words = []
    for xmli in xml_items:
        words.append(xmli.text.lower().split())

    words_len = (list(filter(lambda x: len(x) > 6, sum(words, []))))
    print(*sorted(set(words_len), key=lambda word: (-words_len.count(word), word))[:10], sep='\n')

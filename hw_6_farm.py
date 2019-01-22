def summary_weight(animals_list):
    sum_weight = 0
    for animal in animals_list:
        sum_weight += animal.weight
    print('Общий вес всех животных: {} кг'.format(sum_weight))


def heaviest_animal(animals):
    animals_list = []
    for animal in animals:
        animals_list.append([animal.name, animal.weight])
        animals_list.sort(key=lambda i: i[1], reverse=True)
    print('Самое тяжелое животное: {} с весом {} кг'.format(animals_list[0][0], animals_list[0][1]))


class Animal:
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight

    def eat(self):
        print("Вы покормили {}.".format(self.name))
        self.weight += 1


class Goose(Animal):
    def speak(self):
        print('{}: Га-га-га!'.format(self.name))

    def action(self):
        print('Вы собрали яйца у {}.'.format(self.name))


class Cow(Animal):
    def speak(self):
        print('Мууууу!'.format(self.name))

    def action(self):
        print('Вы подоили корову {}.'.format(self.name))


class Goat(Cow, Animal):
    def speak(self):
        print('{}: Меееее!'.format(self.name))

    def action(self):
        print('Вы подоили козу {}.'.format(self.name))


class Sheep(Animal):
    def speak(self):
        print('{}: Бееее!'.format(self.name))

    def action(self):
        print('Вы постригли овцу {}.'.format(self.name))


class Chicken(Goose, Animal):
    def speak(self):
        print('{}: Ко-Ко-Ко!'.format(self.name))


class Duck(Goose, Animal):
    def speak(self, name):
        print('{}: Кря-Кря!'.format(self.name))


gray_goose = Goose('Серый', 6, )
white_goose = Goose('Белый', 8)
cow_manka = Cow('Манька', 250)
goat_horns = Goat('Рога', 45)
goat_hooves = Goat('Копыта', 40)
sheep_barry = Sheep('Барашек', 28)
sheep_curvy = Sheep('Кудрявый', 25)
chicken_koko = Chicken('Ко-Ко', 3)
chicken_kuku = Chicken('Кукареку', 2)
krya_duck = Duck('Кряква', 4)

animals = [gray_goose,
           white_goose,
           cow_manka,
           goat_horns,
           goat_hooves,
           sheep_barry,
           sheep_curvy,
           chicken_koko,
           chicken_kuku,
           krya_duck]

for animal in animals:
    print('Имя животного: {}'.format(animal.name))
    animal.eat()
    animal.action()
    print()

summary_weight(animals)
heaviest_animal(animals)

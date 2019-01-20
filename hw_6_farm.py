
# Со всеми животными вам необходимо как-то взаимодействовать:

# кормить
# корову и коз доить
# овец стричь
# собирать яйца у кур, утки и гусей
# различать по голосам(коровы мычат, утки крякают и т.д.)
# Задача №1
# Нужно реализовать классы животных, не забывая использовать наследование, определить общие методы взаимодействия с животными и дополнить их в дочерних классах, если потребуется.
#
# Задача №2
# Для каждого животного из списка должен существовать экземпляр класса. Каждое животное требуется накормить и подоить/постричь/собрать яйца, если надо.
#
# Задача №3
# У каждого животного должно быть определено имя(self.name) и вес(self.weight).
#
# Необходимо посчитать общий вес всех животных(экземпляров класса);
# Вывести название самого тяжелого животного.



class Animal:
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight

    def speak(self):
        print("{}: ".format(self.name))
        print("{}: I'm a little fat, now weigh {} pounds".format(self.name, self.weight))
        print()

    def action(self, user):
        print("{}: Let's drink some beer, {}...gulp-gulp".format(self.name, user))
        print()

    def eat(self):
        print("Вы покормили {}.".format(self.name))
        print()

#
# class Me:
#     name = 'Дядюшки Джо'
#
#     def want_eggs(self, obj):
#
#         print("I: Give me some eggs, {}".format(obj.name))
#
#         if type(obj) == Goose or type(obj) == Chicken or type(obj) == Duck:
#             obj.give_eggs(self.name)
#         else:
#             print("Sorry, but {} can`t do eggs".format(obj.name))
#
#     def feed(self, obj):
#         print('Here some food, {}'.format(obj.name))
#         obj.eat()


class Goose(Animal):
    def speak(self):
        print('{}: Га-га-га!'.format(self.name))
        print()

    def action(self):
        print('The {} eating scrumble eggs'.format(self.name))
        print()

    def give_eggs(self):
        print("Now, {} have few eggs from {}".format(self.name))


class Cow(Animal):
    def speak(self):
        print('Moooooooooo, my name is {}! Moooooooooo'.format(self.name))
        print()

    def action(self):
        print('The {} gives milk'.format(self.name))
        print()


class Goat(Cow, Animal):
    def speak(self):
        print('Buaaaaa, buaa, my name is {}! I am goat!'.format(self.name))
        print()


class Sheep(Animal):
    def speak(self):
        print('{}: Бееее!'.format(self.name))
        print()

    def action(self):
        print('{} shears a {}, now we have some wool'.format(self.name))
        print()


class Chicken(Goose, Animal):
    def speak(self):
        print('Ко-Ко-Ко!'.format(self.name))
        print()


class Duck(Goose, Animal):
    def speak(self, name):
        print('{}: Кря-Кря!'.format(self.name))
        print()


gray_goose = Goose('Серый', 6)
white_goose = Goose('Белый', 8)
cow = Cow('Манька', 250)
goat_horns = Goat('Рога', 45)
goat_hooves = Goat('Копыта', 40)
sheep_barry = Sheep('Барашек', 28)
sheep_curvy = Sheep('Кудрявый', 25)
chicken_koko = Chicken('Ко-Ко', 3)
chicken_kuku = Chicken('Кукареку', 2)
krya_duck = Duck('Кряква', 4)

Duck.speak(Duck)



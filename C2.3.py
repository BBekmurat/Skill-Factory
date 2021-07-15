# создадим класс собаки
class Dog:
    _happiness = 10

    def __init__(self, name, age):
        self.name = name
        self.age = age

    # Создадим свойство human_age, которое будет переводить возраст животного в человечески
    @property # Тот самый магический декоратор
    def human_age(self):
        return self.age * 7.3

    #добавим новое поле = шкала счастья
    @property
    def happiness(self):
        return self._happiness

    # с помощью декоратора setter мы можем неявно передать во второй
    # аргумент значение, находящееся справа от равно, а не закидывать это
    # значение в скобки, как мы это делали в модуле C1, когда не знали о
    # декораторах класса
    @happiness.setter
    # допустим, мы хотим, чтобы счатье питомца измерялось шкалой от 0 до 100
    def happiness(self, value):
        if value <= 100 and value >= 0:
            self._happiness = value
        else:
            raise ValueError("Happiness must be between 0 ... 100")

jane = Dog("jane", 4)
# т.к. метод помечен декоратором property, то нам надо вызывать этот метод чтобы получить результат
jane.happiness = 100    # осчастливим нашу собаку
print(jane.happiness)

class ParentClass:

    @classmethod
    def method(cls, arg):
        print("%s classmethod. %d" % (cls.__name__, arg))

    @classmethod
    def call_original_method(cls):
        cls.method(5)

    def call_class_method(self):
        self.method(10)

class ChildClass(ParentClass):

    @classmethod
    def call_original_method(cls):
        cls.method(6)


#Вызываем методы класса через класс
ParentClass.method(0) # ParentClassclassmethod. 0
ParentClass.call_original_method() # ParentClassclassmethod. 5

ChildClass.method(0) # ChildClassclassmethod. 0
ChildClass.call_original_method() #ChildClassclassmethod. 6

# Вызываем методы класса через объект.
my_obj = ParentClass()
my_obj.method(1) # ParentClassclassmethod. 0
my_obj.call_class_method()  #ParentClassclassmethod. 10

class Square:
    _a = None
    def __init__(self, a):
        self.a = a
    @property
    def a(self):
        return self._a
    @a.setter
    def a(self, value):
        if value > 0:
            self._a = value
    @property
    def area(self):
        return self.a**2
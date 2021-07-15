class StaticClass:

    @staticmethod # помечаем метод который мы хотим сделать статичным декоратором @staticmethod
    def bar():
        print("bar")

f = StaticClass()
f.bar()             # вызывать статические методы через объекты так же никто не запрещает

#StaticClass.bar()

class Square:
    def __init__(self, side):
        self.side = side
        
class SquareFactory:
    @staticmethod
    def create_square(side):
        return Square(side)

sq1 = SquareFactory.create_square(1)
print(sq1.side)
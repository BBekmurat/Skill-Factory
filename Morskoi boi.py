from random import randint


class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return "Не возможно стрелять вне поля"


class BoardUsedException(BoardException):
    def __str__(self):
        return "Невозможно стрелять в одну и ту же точку"


class BoardWrongShipException(BoardException):
    pass


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, different):
        return self.x == different.x and self.y == different.y

    def __repr__(self):
        return f"({self.x}, {self.y})"


class Ship:
    def __init__(self, ship_bow, length, orient):
        self.ship_bow = ship_bow
        self.length = length
        self.orient = orient
        self.lives = length

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.length):
            cur_x = self.ship_bow.x
            cur_y = self.ship_bow.y

            if self.orient == 0:
                cur_x += i

            elif self.orient == 1:
                cur_y += i

            ship_dots.append(Dot(cur_x, cur_y))

        return ship_dots

    def shot_down(self, shot):
        return shot in self.dots


class Board:
    def __init__(self, hid=False, size=6):
        self.size = size
        self.hid = hid

        self.count = 0

        self.field = [["O"] * size for _ in range(size)]

        self.taken = []
        self.ships = []

    def add_ship(self, ship):

        for d in ship.dots:
            if self.out(d) or d in self.taken:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = "*"
            self.taken.append(d)

        self.ships.append(ship)
        self.contour(ship)

    def contour(self, ship, verb=False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.taken:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.taken.append(cur)

    def __str__(self):
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            res += f"\n{i + 1} | " + " | ".join(row) + " |"

        if self.hid:
            res = res.replace("*", "O")
        return res

    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def shot(self, d):
        if self.out(d):
            raise BoardOutException()

        if d in self.taken:
            raise BoardUsedException()

        self.taken.append(d)

        for ship in self.ships:
            if d in ship.dots:
                ship.lives -= 1
                self.field[d.x][d.y] = "X"
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print("Корабль противника уничтожен")
                    return False
                else:
                    print("Корабль противника поврежден")
                    return True

        self.field[d.x][d.y] = "."
        print("Выстрел мимо")
        return False

    def begin(self):
        self.taken = []


class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        pass

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        print(f"Ход AI: {d.x + 1} {d.y + 1}")
        return d


class User(Player):
    def ask(self):
        while True:
            cords = input("Ваш ход: ").split()

            if len(cords) != 2:
                print(" Введите 2 координаты! ")
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print(" Введите числа! ")
                continue

            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)


class Game:
    def __init__(self, size=6):
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hid = True

        self.ai = AI(co, pl)
        self.us = User(pl, co)

    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board

    def random_place(self):
        ships_order = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attempts = 0
        for n in ships_order:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), n, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    @staticmethod
    def greet():
        print("---------------------")
        print("  Вас приветствует   ")
        print("        игра         ")
        print("    МОРСКОЙ БОЙ      ")
        print("---------------------")
        print("необходимо ввести:x y")
        print("  x - номер строки   ")
        print("  y - номер столбца  ")
        print(" Координаты от 1 до 6")

    def loop(self):
        num = 0
        while True:
            print("-" * 20)
            print("Поле пользователя:")
            print(self.us.board)
            print("-" * 20)
            print("Поле AI:")
            print(self.ai.board)
            if num % 2 == 0:
                print("-" * 20)
                print("Ход пользователя!")
                repeat = self.us.move()
            else:
                print("-" * 20)
                print("Ход AI!")
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.count == 7:
                print("-----------------------------")
                print("Пользователь выиграл!")
                break

            if self.us.board.count == 7:
                print("-----------------------------")
                print("Компьютер AI!")
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()


lets_play = Game()
lets_play.start()
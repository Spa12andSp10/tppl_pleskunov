import re

class StackMachine():

    """Реализация стэковой машины"""

    def __init__(self):
        self.stack = []
        self.result = []

    def add(self, op1: float, op2: float) -> None:

        """Сложение двух операндов"""

        self.stack = self.stack[:-2]
        self.stack.append(op1 + op2)

    def sub(self, op1: float, op2: float) -> None:

        """Разность двух операндов"""

        self.stack = self.stack[:-2]
        self.stack.append(op1 - op2)

    def mul(self, op1: float, op2: float) -> None:

        """Умножение двух операндов"""

        self.stack = self.stack[:-2]
        self.stack.append(op1 * op2)

    def div(self, op1: float, op2: float) -> None:

        """Деление двух операндов"""

        self.check_zero(op2)
        self.stack = self.stack[:-2]
        self.stack.append(op1 / op2)

    def tilda(self, op1: float, op2: float) -> None:

        """Реализация специального оператора тильда (~)"""

        if op1 != 0 and op2 != 0:
            self.stack = self.stack[:-2]
            self.stack.append(abs(op1 - op2))
        if op1 == 0 or op2 == 0:
            total = sum(self.stack) ** 2
            self.stack = []
            self.stack.append(total)

    def calculate(self, string: str) -> tuple[list[str], float]:

        """Реализация основного пересчета"""

        self.stack = []
        self.result = []
        count = 1
        self.check_empty_string(string)
        value = string.split(" ")
        self.check_incorrect_value(value)

        for token in value:
            if token in "+-*/~":
                self.check_two_operands_in_stack(self.stack, token)
                if token == "+":
                    self.add(self.stack[-2], self.stack[-1])
                elif token == "-":
                    self.sub(self.stack[-2], self.stack[-1])
                elif token == "*":
                    self.mul(self.stack[-2], self.stack[-1])
                elif token == "/":
                    self.div(self.stack[-2], self.stack[-1])
                elif token == "~":
                    self.tilda(self.stack[-2], self.stack[-1])
            else:
                self.stack.append(float(token))

            self.result.append(f"Шаг {count}, стэк {self.stack}")
            count += 1

        self.check_last_element(self.stack)
            
        return (self.result, self.stack[0])

    def check_incorrect_value(self, value: list) -> None:

        """Проверка на неккоректное значение в строке"""

        operators = {"+", "-", "*", "/", "~"}
        for i in value:
            if i in operators:
                continue
            try:
                float(i)
            except ValueError:
                raise ValueError("Некорректное значение в массиве!")
            
    def check_last_element(self, value: list) -> None:

        """Проверка, что остался именно последний элемент в стэке"""

        if len(value) != 1:
            raise ArithmeticError("Остается не 1 число, проверте строку!")

    def check_two_operands_in_stack(self, value: list, token: str) -> None:

        """Провекрка на то, что есть два операнда для применения операции"""

        if len(value) < 2:
            raise ValueError(
                f"Недостаточно операндов для операции '{token}'!"
            )

    def check_empty_string(self, value: str) -> None:

        """Проверка на пустоту строки"""

        if value == "":
            raise ValueError("Строка пустая!")

    
    def check_zero(self, op) -> None:

        """Проверка на деление на ноль"""

        if op == 0:
            raise ZeroDivisionError("Деление на ноль!")




def main() -> None:
    print("Стэковая Машина") # pragma: no cover
    print("""
    Принцип работы стековой машины

    - Обрабатывает арифметические операции: `+`, `-`, `/`, `*`
    - Обрабатывает специальный оператор `~`
    - Операнды и операции разделены пробелами
    - Операнды должны быть числами (целыми (как положительными, так и отрицательными) или дробными (с плавающей точкой)) или нулем
    - Недопускается деление на 0
    - Операции не могут в быть первым или вторым элементом
    """) # pragma: no cover
    print("""
    Описание оператора `~`

    Если оба операнда не равны 0: вычислить модуль разницы `|x - y|` и положить результат обратно в стек.
    Если хотя бы один из операндов равен 0: вычисляет сумму всех значений в стеке, возводит её в квадрат и кладет результат обратно в стек
    """) # pragma: no cover

    stack_machine = StackMachine() # pragma: no cover
    while True: # pragma: no cover
        try: # pragma: no cover
            string = input("Введите строку формата '2 3 +' : ") # pragma: no cover
            result, last_element = stack_machine.calculate(string) # pragma: no cover
            for step in result: # pragma: no cover
                print(step) # pragma: no cover
            print(f"Выражение {string} = {last_element}") # pragma: no cover
            break # pragma: no cover
        except ZeroDivisionError:
            print("В строке происходит деление на ноль!") # pragma: no cover
        except ValueError: # pragma: no cover
            print("Кажется, у вас проблемы со строкой!") # pragma: no cover
        except IndexError: # pragma: no cover
            print("Кажется, в стеке недостаточно операндов!") # pragma: no cover
        except ArithmeticError: # pragma: no cover
            print("Остается не 1 число, проверьте строку!") # pragma: no cover
        except Exception as e: # pragma: no cover
            print(f"Непредвиденная ошибка: {e}") # pragma: no cover


if __name__ == "__main__":
    main() # pragma: no cover


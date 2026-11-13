import sys
import os

class Tokenizer:

    """Токенизатор"""

    def __init__(self):
        self.result = []
        self.data = ""

    def numbers(self, value: str, pos: int, c: str):
        """Распознование целых или вещественных чисел"""
        start = pos
        my_str = c
        is_float = False
        pos += 1
        while pos < len(value) and (value[pos].isdigit() or value[pos] == "."):
            if value[pos] == ".":
                if is_float:
                    break
                is_float = True
            my_str += value[pos]
            pos += 1
        finish = pos

        if pos < len(value) and (value[pos].isalpha() or value[pos] == "_"):
            token_type = ""
        else:
            token_type = "FLOAT" if is_float else "INT"

        return (token_type, pos, start, finish, my_str)
    def identifiers_or_keywords(self, value: str, pos: int, c: str):
        """Распознование ключевых слов или индентификаторов"""
        keywords = {"if", "else", "while", "return", "for", "def"}
        start = pos
        my_str = c
        pos += 1
        while pos < len(value) and (value[pos].isalnum() or value[pos] == "_"):
            my_str += value[pos]
            pos += 1
        finish = pos
        token = "KEYWORD" if my_str in keywords else "IDENT"
        return (token, pos, start, finish, my_str)

    def string_token(self, value: str, pos: int, c: str):
        """Распознавание строк"""
        start = pos
        my_str = c
        pos += 1
        while pos < len(value) and value[pos] != '"':
            my_str += value[pos]
            pos += 1
        if pos >= len(value):
            finish = pos
            return ("", pos, start, finish, my_str)
        my_str += value[pos]
        pos += 1
        finish = pos
        return ("STRING", pos, start, finish, my_str)

    def comment(self, value: str, pos: int):
        """Пропуск комментов"""
        while pos < len(value) and value[pos] != "\n":
            pos += 1
        return pos

    def load(self, filename: str):
        """Загрузка файла"""
        if not os.path.exists(filename):
            raise FileNotFound(filename)
        with open(filename, "r", encoding="utf-8") as file:
            data = file.read()
        return data


    def tokenizer(self, filename: str) -> list:
        """Основная функция для токенизации. В ней дополнительно распознаются разделители и операции"""
        string = self.load(filename)
        if os.path.getsize(filename) == 0:
            raise FileIsEmpty(filename)
        pos = 0
        line, col = 1, 1
        cnt_p, cnt_b = 0, 0

        while pos < len(string):
            c = string[pos]

            if c.isdigit():
                token, pos, start, finish, my_str = self.numbers(string, pos, c)
                self.result.append(f"({token}, {my_str} {line}:{col})")
                col += finish - start
                if token == "":
                    raise IdentifierNotStartWithDigit(filename, line, col)
                continue

            if c.isalpha() or c == "_":
                token, pos, start, finish, my_str = self.identifiers_or_keywords(string, pos, c)
                self.result.append(f"({token}, {my_str} {line}:{col})")
                col += finish - start
                continue

            if c == '"':
                token, pos, start, finish, my_str = self.string_token(string, pos, c)
                self.result.append(f"({token}, {my_str} {line}:{col})")
                col += finish - start
                if token == "":
                    raise UnclosedParenthesesOrQuotationMarks(filename, line, col)
                continue

            if c in "+-*/":
                self.result.append(f"(OP, {c} {line}:{col})")
                pos += 1
                col += 1
                continue

            if c in "=<>!":
                start = pos
                pos += 1
                if pos < len(string) and string[pos] == "=":
                    c += "="
                    pos += 1
                self.result.append(f"(OP, {c} {line}:{col})")
                col += pos - start
                continue

            if c in "(){},;":
                self.result.append(f"(SEP, {c} {line}:{col})")
                pos += 1
                col += 1
                if c == "(":
                    cnt_p += 1
                elif c == "{":
                    cnt_b += 1
                elif c == ")":
                    cnt_p -= 1
                elif c == "}":
                    cnt_b -= 1
                continue

            if c == "#":
                pos = self.comment(string, pos)

            elif c == "\n":
                line += 1
                col = 1
                pos += 1

            elif c in " \t\r":
                pos += 1
                col += 1

            else:
                raise LexicalError(filename, line, col, c)
        if cnt_p != 0 or cnt_b != 0:
            raise UnclosedParenthesesOrQuotationMarks(filename, line, col)
        return self.result

class LexicalError(Exception):
    """Класс для распознования лексической ошибки"""
    def __init__(self, filename: str, line: int, col: int, char: str):
        self.filename = filename
        self.line = line
        self.col = col
        self.char = char
        super().__init__(
            f"{filename}:{line}:{col} lexical: unexpected character '{char}'"
        )

class UnclosedParenthesesOrQuotationMarks(Exception):
    """Класс для распознования незакрытых скобок или кавычек (это считается ошибкой)"""
    def __init__(self, filename: str, line: int, col: int):
        self.filename = filename
        self.line = line
        self.col = col
        super().__init__(
            f"{filename}:{line}:{col} lexical: unclosed parenthesis or quotation mark"
        )

class IdentifierNotStartWithDigit(Exception):
    """Класс, который выводит ошибку, если переменная начинается с цифры"""
    def __init__(self, filename: str, line: int, col: int):
        self.filename = filename
        self.line = line
        self.col = col
        super().__init__(
            f"{filename}:{line}:{col} lexical: Identifier cannot begin with a number"
        )

class FileNotFound(Exception):
    """Класс ошибки ненайденного файла"""
    def __init__(self, filename: str):
        self.filename = filename
        super().__init__(
            f"{filename}:0:0 lexical: File Not found"
        )

class FileIsEmpty(Exception):
    """Класс ошибки пустого файла"""
    def __init__(self, filename: str):
        self.filename = filename
        super().__init__(
            f"{filename}:0:0 lexical: File is empty"
        )

def main() -> int: # pragma: no cover

    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <file>", file=sys.stderr)
        return 6

    if sys.argv[1] == "-help" or sys.argv[1] == "-h":
        print("""Программа представляет собой реализацию токенизатора.""")
        print("""Лексический анализатор (токенизатор), который превращает строку исходного кода в последовательность токенов.
Токенизатор должен распознавать:

    - идентификаторы (последовательность букв, цифр и `_`, не начинающаяся с цифры);
    - ключевые слова: `if`, `else`, `while`, `return`, `for`, `def`;
    - целые и вещественные литералы;
    - строковые литералы в двойных кавычках;
    - операторы: `+ - * / = < > == <= >=`;
    - разделители: `( ) { } , ;`.

Пробелы, символы табуляции и комментарии (от `#` до конца строки) пропускаются.""")

        print("""Запуск команды: python main.py название_файла или python3 main.py название_файла""")
        sys.exit()

    try:
        res = Tokenizer().tokenizer(sys.argv[1])
        for r in res:
            print(r)
    except LexicalError as e:
        print(e, file=sys.stderr)
        return 1
    except UnclosedParenthesesOrQuotationMarks as e:
        print(e, file=sys.stderr)
        return 2
    except IdentifierNotStartWithDigit as e:
        print(e, file=sys.stderr)
        return 3
    except FileNotFound as e:
        print(e, file=sys.stderr)
        return 4
    except FileIsEmpty as e:
        print(e, file=sys.stderr)
        return 5
    except OSError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 6


if __name__ == "__main__":
    sys.exit(main()) # pragma: no cover

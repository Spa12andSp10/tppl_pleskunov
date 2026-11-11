import sys
import pytest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from main import Tokenizer, main, LexicalError, UnclosedParenthesesOrQuotationMarks, IdentifierNotStartWithDigit, FileIsEmpty, FileNotFound

@pytest.fixture
def make_file(tmp_path):

    def _make(content: str, name: str = "input.txt") -> str:
        p = tmp_path / name
        p.write_text(content, encoding="utf-8")
        return str(p)

    return _make

def tokens(filename: str) -> list[str]:
    return Tokenizer().tokenizer(filename)

def test_correct_string(make_file):
    f = make_file("x = y * 2 + z * 3\n")
    assert tokens(f) == [
            "(IDENT, x 1:1)",
            "(OP, = 1:3)",
            "(IDENT, y 1:5)",
            "(OP, * 1:7)",
            "(INT, 2 1:9)",
            "(OP, + 1:11)",
            "(IDENT, z 1:13)",
            "(OP, * 1:15)",
            "(INT, 3 1:17)",
        ]

def test_correct_string_with_float(make_file):
    f = make_file("x = y * 2.3 + z * 3\n")
    assert tokens(f) == [
            "(IDENT, x 1:1)",
            "(OP, = 1:3)",
            "(IDENT, y 1:5)",
            "(OP, * 1:7)",
            "(FLOAT, 2.3 1:9)",
            "(OP, + 1:13)",
            "(IDENT, z 1:15)",
            "(OP, * 1:17)",
            "(INT, 3 1:19)",
        ]

def test_correct_string_with_keyword(make_file):
    f = make_file("if x\n")
    assert tokens(f) == ["(KEYWORD, if 1:1)", "(IDENT, x 1:4)"]

def test_correct_string_with_str(make_file):
    f = make_file('if x == "hello"\n')
    assert tokens(f) == [
        "(KEYWORD, if 1:1)",
        "(IDENT, x 1:4)",
        "(OP, == 1:6)",
        '(STRING, "hello" 1:9)',
    ]

def test_corrrect_string_with_parentheses(make_file):
    f = make_file("(a { b })\n")
    assert tokens(f) == [
        "(SEP, ( 1:1)",
        "(IDENT, a 1:2)",
        "(SEP, { 1:4)",
        "(IDENT, b 1:6)",
        "(SEP, } 1:8)",
        "(SEP, ) 1:9)",
    ]

def test_correct_string_with_comment(make_file):
    f = make_file("x # this is comment\ny\n")
    assert tokens(f) == ["(IDENT, x 1:1)", "(IDENT, y 2:1)"]


def test_correct_string_with_lines(make_file):
    f = make_file("a\nb\nc\n")
    assert tokens(f) == [
        "(IDENT, a 1:1)",
        "(IDENT, b 2:1)",
        "(IDENT, c 3:1)",
    ]

def test_correct_test_with_op(make_file):
    f = make_file("a == b != c <= d >= e\n")
    assert tokens(f) == [
        "(IDENT, a 1:1)",
        "(OP, == 1:3)",
        "(IDENT, b 1:6)",
        "(OP, != 1:8)",
        "(IDENT, c 1:11)",
        "(OP, <= 1:13)",
        "(IDENT, d 1:16)",
        "(OP, >= 1:18)",
        "(IDENT, e 1:21)",
    ]


def test_correct_test_with_sep(make_file):
    f = make_file("f(a, b);\n")
    assert tokens(f) == [
        "(IDENT, f 1:1)",
        "(SEP, ( 1:2)",
        "(IDENT, a 1:3)",
        "(SEP, , 1:4)",
        "(IDENT, b 1:6)",
        "(SEP, ) 1:7)",
        "(SEP, ; 1:8)",
    ]

def test_unexpected_char(make_file):
    f = make_file("x = @\n")
    with pytest.raises(LexicalError) as exc:
        Tokenizer().tokenizer(f)
    assert "unexpected character '@'" in str(exc.value)


def test_unclosed_paren(make_file):
    f = make_file("f(x\n")
    with pytest.raises(UnclosedParenthesesOrQuotationMarks):
        Tokenizer().tokenizer(f)


def test_unclosed_brace(make_file):
    f = make_file("{ x\n")
    with pytest.raises(UnclosedParenthesesOrQuotationMarks):
        Tokenizer().tokenizer(f)


def test_unclosed_string(make_file):
    f = make_file('s = "abc\n')
    with pytest.raises(UnclosedParenthesesOrQuotationMarks):
        Tokenizer().tokenizer(f)


def test_ident_starts_with_digit(make_file):
    f = make_file("123abc\n")
    with pytest.raises(IdentifierNotStartWithDigit):
        Tokenizer().tokenizer(f)


def test_number_with_two_dots(make_file):
    f = make_file("x = 3.3.5\n")
    with pytest.raises((LexicalError, IdentifierNotStartWithDigit)):
        Tokenizer().tokenizer(f)

def test_empty_file(make_file):
    f = make_file("")
    with pytest.raises((LexicalError, FileIsEmpty)):
        Tokenizer().tokenizer(f)

def test_file_not_found(make_file):
    f = "tests/txt"
    with pytest.raises((LexicalError, FileNotFound)):
        Tokenizer().tokenizer(f)
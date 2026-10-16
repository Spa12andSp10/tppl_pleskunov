import pytest
from main import StackMachine


@pytest.fixture
def machine():
    return StackMachine()


def test_evaluate_basic(machine):
    # Действие
    _, result = machine.calculate("3 0 4 ~ 2 ~")
    # Проверки
    assert result == 47.0


def test_evaluate_addition(machine):
    # Действие
    _, result = machine.calculate("2 3 +")
    # Проверки
    assert result == 5.0


def test_evaluate_subtraction(machine):
    # Действие
    _, result = machine.calculate("10 4 -")
    # Проверки
    assert result == 6.0


def test_evaluate_multiplication(machine):
    # Действие
    _, result = machine.calculate("3 4 *")
    # Проверки
    assert result == 12.0


def test_evaluate_division(machine):
    # Действие
    _, result = machine.calculate("10 2 /")
    # Проверки
    assert result == 5.0


def test_evaluate_float_operands(machine):
    # Действие
    _, result = machine.calculate("3.5 2 +")
    # Проверки
    assert result == 5.5


def test_evaluate_negative_operand(machine):
    # Действие
    _, result = machine.calculate("-2 5 +")
    # Проверки
    assert result == 3.0


def test_tilda_both_nonzero(machine):
    # Действие
    _, result = machine.calculate("10 3 ~")
    # Проверки
    assert result == 7.0


def test_tilda_with_zero_squares_sum(machine):
    # Действие
    _, result = machine.calculate("3 0 4 ~")
    # Проверки
    assert result == 49.0


def test_chain_expression(machine):
    # Действие
    _, result = machine.calculate("2 3 + 4 *")
    # Проверки
    assert result == 20.0


def test_empty_string(machine):
    # Действие
    # Проверки
    with pytest.raises(ValueError):
        machine.calculate("")


def test_incorrect_symbols(machine):
    # Действие
    # Проверки
    with pytest.raises(ValueError):
        machine.calculate("a b +")


def test_incorrect_value_letters(machine):
    # Действие
    # Проверки
    with pytest.raises(ValueError):
        machine.calculate("2 0/")


def test_incorrect_value_garbage(machine):
    # Действие
    # Проверки
    with pytest.raises(ValueError):
        machine.calculate("2 x +")


def test_not_enough_operands_for_operator(machine):
    # Действие
    # Проверки
    with pytest.raises(ValueError):
        machine.calculate("+ 2 3")


def test_single_operand_plus(machine):
    # Действие
    # Проверки
    with pytest.raises(ValueError):
        machine.calculate("5 +")


def test_zero_division(machine):
    # Действие
    # Проверки
    with pytest.raises(ZeroDivisionError):
        machine.calculate("1 0 /")


def test_zero_division_float(machine):
    # Действие
    # Проверки
    with pytest.raises(ZeroDivisionError):
        machine.calculate("5 0.0 /")


def test_no_one_element_in_stack(machine):
    # Действие
    # Проверки
    with pytest.raises(ArithmeticError):
        machine.calculate("2 2 + 1")


def test_only_operands_no_operator(machine):
    # Действие
    # Проверки
    with pytest.raises(ArithmeticError):
        machine.calculate("1 2 3")


def test_state_reset_between_calls(machine):
    # Действие
    _, first = machine.calculate("2 3 +")
    _, second = machine.calculate("4 5 +")
    # Проверки
    assert first == 5.0
    assert second == 9.0


def test_state_reset_after_error(machine):
    # Подготовка
    # Действие
    with pytest.raises(ZeroDivisionError):
        machine.calculate("1 0 /")
    _, result = machine.calculate("2 3 +")
    # Проверки
    assert result == 5.0


def test_result_steps_count(machine):
    # Действие
    result, _ = machine.calculate("2 3 +")
    # Проверки
    assert len(result) == 3


def test_result_step_format(machine):
    # Действие
    result, _ = machine.calculate("2 3 +")
    # Проверки
    assert result[0] == "Шаг 1, стэк [2.0]"
    assert result[1] == "Шаг 2, стэк [2.0, 3.0]"
    assert result[2] == "Шаг 3, стэк [5.0]"
from lesson10.calculations import numbers_sum
from lesson10.capital import check_guess


def testing_numbers_sum():
    assert numbers_sum(2, 3) == 5
    return "testing_numbers_sum() passed successfully"


def test_check_guess():
    assert check_guess("Ljubljana", "Slovenia", {"Slovenia": "Ljubljana"}) == True
    return "test_check_guess() passed successfully."

print testing_numbers_sum()
print test_check_guess()
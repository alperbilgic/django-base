import random
import string


def random_alphanumeric_string(length: int) -> str:
    letters = string.ascii_lowercase + string.digits + string.ascii_uppercase
    result_str = "".join(random.choice(letters) for i in range(length))
    return result_str


def random_numeric_string(length: int) -> str:
    letters = string.digits
    result_str = "".join(random.choice(letters) for i in range(length))
    return result_str

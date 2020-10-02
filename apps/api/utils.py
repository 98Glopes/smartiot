import random
import string


def get_random_string():
    letters = string.ascii_letters + string.digits
    result_str = ''.join(random.choice(letters) for i in range(4))
    return result_str

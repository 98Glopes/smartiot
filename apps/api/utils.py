import random
import string


def get_random_string(n=4):
    letters = string.ascii_letters + string.digits
    result_str = ''.join(random.choice(letters) for i in range(n))
    return result_str

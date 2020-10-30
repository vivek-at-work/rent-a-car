import random
import string


def booking_number_generator(size=6, chars=string.ascii_uppercase + string.digits):
    # TODO: This is prone to db collissions we need better ganerators
    return ''.join(random.choice(chars) for _ in range(size))

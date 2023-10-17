import random
import string


def generatePassword():
    length = random.randint(30, 45)
    characters = string.ascii_letters + string.digits + \
        string.punctuation
    password = ''.join(random.choice(characters)
                       for _ in range(length))
    return password

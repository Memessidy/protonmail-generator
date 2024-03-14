from faker import Faker
import random
import string

fake = Faker()


def generate_name_and_lastname() -> list[str]:
    random_name = fake.name().split()
    while len(random_name) != 2:
        random_name = fake.name().split()
    return random_name


def generate_password(min_len=10, max_len=30, vals=string.ascii_letters + string.digits) -> str:
    random_number = random.randint(min_len, max_len)
    password = ''.join(random.choices(vals, k=random_number))
    return password


def return_user_data() -> tuple[str, str]:
    password = generate_password()
    name_and_lastname = (generate_password(min_len=5, max_len=10, vals=string.ascii_lowercase)
                         .join(generate_name_and_lastname()).lower())

    return name_and_lastname, password

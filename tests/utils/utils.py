import random
import string
from datetime import datetime

from faker import Faker

fake = Faker()
Faker.seed(0)


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=10))


def random_datetime() -> datetime:
    return fake.iso8601()


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


def random_name() -> str:
    return random_lower_string()

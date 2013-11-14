from models import User
import factory
import random

class UserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = User

    remote_id = factory.Sequence(lambda n: n)
    sex = random.choice([1,2])
    wall_comments = False
from models import User
import factory
import random

class UserFactory(factory.DjangoModelFactory):

    remote_id = factory.Sequence(lambda n: n)
    sex = random.choice([1,2])

    class Meta:
        model = User

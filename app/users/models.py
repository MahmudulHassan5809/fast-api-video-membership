import uuid
from cassandra.cqlengine.models import Model
from cassandra.cqlengine import columns


from app.config import get_settings

settings = get_settings()

class User(Model):
    __keyspace__ = settings.keyspace
    email = columns.Text(primary_key=True)
    user_id = columns.UUID(primary_key=True, default=uuid.uuid1)
    password = columns.Text()

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"user_email={self.email}, user_id={self.user_id})"
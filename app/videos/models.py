import uuid
from app.config import get_settings
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from app.users.exceptions import InvalidUserIDException

from app.users.models import User
from app.videos.exceptions import InvalidYouTubeVideoURLException, VideoAlreadyAddedException
from app.videos.extractors import extract_video_id

settings = get_settings()


class Video(Model):
    __keyspace__ = settings.keyspace
    host_id = columns.Text(primary_key=True)
    db_id = columns.UUID(primary_key=True, default=uuid.uuid1)
    host_service = columns.Text(default='youtube')
    title = columns.Text()
    url = columns.Text()
    user_id = columns.UUID()

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"Video(title={self.title}, host_id={self.host_id}, host_service={self.host_service})"

    def as_data(self):
        return {f"{self.host_service}_id": self.host_id, "path": self.path, "title": self.title}

    @property
    def path(self):
        return f"/videos/{self.host_id}"

    @staticmethod
    def add_video(url, user_id=None, **kwargs):
        # extract video_id from url
        # video_id = host_id
        # Service API - YouTube / Vimeo / etc
        host_id = extract_video_id(url)
        if host_id is None:
            raise InvalidYouTubeVideoURLException("Invalid YouTube Video URL")
        user_exists = User.check_exists(user_id)
        if user_exists is None:
            raise InvalidUserIDException("Invalid user_id")

        q = Video.objects.allow_filtering().filter(user_id=user_id, host_id=host_id)
        if q.count() != 0:
            raise VideoAlreadyAddedException("Video already added")

        return Video.create(host_id=host_id, user_id=user_id, url=url, **kwargs)

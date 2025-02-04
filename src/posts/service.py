from src.posts.models import Post
from src.services import BaseService


class PostService(BaseService):
    model = Post
from sqladmin import ModelView

from src.posts.models import Post
from src.users.models import User


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username]


class PostAdmin(ModelView, model=Post):
    column_list = [Post.id, Post.content]

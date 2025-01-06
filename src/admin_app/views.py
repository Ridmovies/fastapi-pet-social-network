from sqladmin import ModelView

from src.post_app.models import Post


class PostAdmin(ModelView, model=Post):
    column_list = [Post.id, Post.content]
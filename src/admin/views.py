from sqladmin import ModelView

from src.posts.models import Post
from src.users.models import User
from src.workout.models import Workout


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username]


class PostAdmin(ModelView, model=Post):
    column_list = [Post.id, Post.content]

class WorkoutAdmin(ModelView, model=Workout):
    column_list = [Workout.id]


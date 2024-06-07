from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=20, unique=True)
    first_name = None
    github_id = models.CharField(max_length=20)

    def create_user(self, username, password, github_id):
        self.username = username
        self.set_password(password)
        self.github_id = github_id
        self.save()

    def get_github_id(self):
        return str(self.github_id)


def run_xd():
    newuser = User()
    newuser.create_user("ethanj23", "ethanj23@gmail.com", "Ethan123")

    ethan_user = User.objects.filter(username="ethanj23").first()
    print(ethan_user.Full_name)
    print(ethan_user.password)


# run_xd()

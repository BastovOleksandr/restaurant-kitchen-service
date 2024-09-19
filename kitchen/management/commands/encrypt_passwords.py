from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password


class Command(BaseCommand):
    help = "Encrypts plain text passwords in the database"

    def handle(self, *args, **kwargs):
        users = get_user_model().objects.all()
        for user in users:
            if not user.password.startswith("pbkdf2_sha256"):
                self.stdout.write(
                    f"Encrypting password for user: {user.username}"
                )
                user.password = make_password(user.password)
                user.save()
        self.stdout.write(
            self.style.SUCCESS("Successfully encrypted all passwords"))

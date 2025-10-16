import getpass
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from django.db import transaction

# IMPORTANT: You MUST change 'Admin.models' to the correct app path
# where your 'Admin' model is defined (e.g., 'Accounts.models' if it's there).
# We are assuming the model is named 'Admin' based on your screenshot.
from Admin.models import Admin


class Command(BaseCommand):
    help = 'Creates a user OR promotes an existing user to superuser/custom admin status.'

    def handle(self, *args, **options):
        User = get_user_model()
        self.stdout.write(self.style.SUCCESS("--- Custom Admin Account Management ---"))

        # --- 1. Get Username ---
        username = input("Enter Username (to create OR promote): ")
        if not username:
            raise CommandError("Username cannot be empty.")

        # Initialize variables to prevent NameError
        user = None
        action = ''

        # --- 2. Check Existence / Get User or Get Creation Data ---
        try:
            # TRY BLOCK: User exists, retrieve it and assign to 'user'
            user = User.objects.get(username=username)
            action = 'Promoted'

            self.stdout.write(self.style.WARNING(f"User '{username}' already exists."))
            confirm = input("Do you want to promote this user to a full admin? (yes/no): ")

            if confirm.lower() not in ['yes', 'y']:
                self.stdout.write("Promotion aborted.")
                return

        except User.DoesNotExist:
            # EXCEPT BLOCK: User does not exist, get creation data
            action = 'Created'
            self.stdout.write("User does not exist. Proceeding to create a new admin account.")

            email = input("Email address (optional): ")

            while True:
                password = getpass.getpass("Password: ")
                password2 = getpass.getpass("Password (again): ")
                if password == password2 and password:
                    break
                self.stderr.write("Error: Passwords must match and cannot be empty.")

            # CREATE USER and assign to 'user'
            user = User.objects.create_user(username=username, email=email, password=password)

        # --- 3. Run Transaction to Set Flags ---
        try:
            with transaction.atomic():

                # a. Django Superuser/Staff status
                user.is_staff = True
                user.is_superuser = True
                user.save()

                # b. Custom Admin status (CRITICAL FIX)
                try:
                    # Try accessing the linked model via the 'admin' accessor (used in templates)
                    admin_profile_instance = getattr(user, 'admin')
                except AttributeError:
                    # If the 'admin' object is missing, create it using the 'Admin' model class
                    admin_profile_instance, created = Admin.objects.get_or_create(user=user)

                    if created:
                        self.stdout.write(self.style.WARNING("Note: Created missing Admin object to set admin status."))

                # Set the custom admin flag
                admin_profile_instance.is_admin = True
                admin_profile_instance.save()

                # --- 4. Success Message ---
                self.stdout.write(self.style.SUCCESS(
                    f"\nSuccessfully {action} custom admin account for '{username}'. Log in to see the dashboard."))

        except Exception as e:
            # Clean up the user if it was created in this run and the transaction failed
            if action == 'Created':
                self.stderr.write(f"Attempting to clean up partially created user: {username}")
                user.delete()
            raise CommandError(f"An error occurred during account management: {e}")
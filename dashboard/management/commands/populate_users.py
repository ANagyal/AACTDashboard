from django.core.management.base import BaseCommand
from django.db import connections
from django.contrib.auth.models import User
from dashboard.models import DashboardUser

class Command(BaseCommand):
    help = "Populates users from AACT DB query"

    def handle(self, *args, **kwargs):
        self.stdout.write("Fetching data from AACT database...")

        with connections['aact'].cursor() as cursor:
            cursor.execute("""
                SELECT nct_id, brief_title, cc.name, cc.email
                FROM studies s
                JOIN central_contacts cc USING (nct_id)
                WHERE cc.email ILIKE '%@%'
                LIMIT 20;
            """)
            rows = cursor.fetchall()

        trial_map = {}
        for nct_id, title, name, email in rows:
            if email not in trial_map:
                trial_map[email] = {
                    "full_name": name,
                    "trials": []
                }
            trial_map[email]["trials"].append({
                "nct_id": nct_id,
                "title": title
            })

        for email, data in trial_map.items():
            user, created = User.objects.get_or_create(username=email, defaults={"email": email})
            if created:
                user.set_password("password")  # Default mock password
                user.save()
                self.stdout.write(f"Created user: {email}")
            else:
                self.stdout.write(f"User already exists: {email}")

            DashboardUser.objects.update_or_create(
                user=user,
                defaults={
                    "full_name": data["full_name"],
                    "trials": data["trials"]
                }
            )

        self.stdout.write(self.style.SUCCESS("Finished populating users."))
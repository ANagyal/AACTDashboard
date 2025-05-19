from django.core.management.base import BaseCommand
from django.db import connections
from django.contrib.auth.models import User
from dashboard.models import DashboardUser

class Command(BaseCommand):
    # Help message for the command
    help = "Populates users from AACT DB query"

    def handle(self, *args, **kwargs):
        # Print out message explaining what the command is currently doing
        self.stdout.write("Fetching data from AACT database...")

        # Fetch data from the AACT database
        with connections['aact'].cursor() as cursor:
            cursor.execute("""
                SELECT
                    s.nct_id,
                    s.brief_title,
                    cc.name AS contact_name,
                    cc.email AS contact_email,

                    s.study_type,
                    s.phase,
                    s.overall_status,
                    s.last_known_status,

                    s.start_date,
                    s.completion_date,

                    s.plan_to_share_ipd,
                    s.source AS sponsor_organization
                FROM studies s
                JOIN central_contacts cc USING (nct_id)
                WHERE cc.email ILIKE '%@%'
                LIMIT 20;
            """)
            rows = cursor.fetchall()

        # Map the retrieved user data for easy trial retrieval
        trial_map = {}
        for (
            nct_id, brief_title, contact_name, contact_email,
            study_type, phase, overall_status, last_known_status,
            start_date, completion_date, 
            plan_to_share_ipd, sponsor_organization
        ) in rows:
            if contact_email not in trial_map:
                trial_map[contact_email] = {
                    "full_name": contact_name,
                    "trials": []
                }
            trial_map[contact_email]["trials"].append({
                "nct_id": nct_id,
                "brief_title": brief_title,
                "study_type": study_type,
                "phase": phase,
                "overall_status": overall_status,
                "last_known_status": last_known_status,
                "start_date": str(start_date) if start_date else None,
                "completion_date": str(completion_date) if completion_date else None,
                "plan_to_share_ipd": plan_to_share_ipd,
                "sponsor_organization": sponsor_organization,
            })
            
        # Create auth.User and DashboardUser instances and use a one-to-one field mapping
        for email, data in trial_map.items():
            user, created = User.objects.get_or_create(username=email, defaults={"email": email})
            if created:
                user.set_password("password")
                user.save()
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
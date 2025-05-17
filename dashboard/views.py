from django.shortcuts import render
from django.db import connection, connections
from django.http import JsonResponse
from django.contrib.auth.models import User

def mock_contact_data(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT nct_id, brief_title, cc.name, cc.email
            FROM ctgov.studies s
            JOIN ctgov.central_contacts cc USING (nct_id)
            WHERE cc.email ILIKE '%%@%%'
            LIMIT 20;
        """)
        rows = cursor.fetchall()
        data = []
        for row in rows:
            nct_id, brief_title, contact_name, email = row
            if email:
                username = email.split('@')[0]
                if not User.objects.filter(username=username).exists():
                    user = User.objects.create_user(username=nct_id, email=email, password='password', first_name=contact_name)
                    user.save()
        return JsonResponse({'created_users': [email for _, _, _, email in rows]})
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import DashboardUser

@login_required
def dashboard_view(request):
    dashboard_user = DashboardUser.objects.get(user=request.user)
    return render(request, 'dashboard/dashboard.html', {
        'dashboard_user': dashboard_user,
        'trials': dashboard_user.trials
    })
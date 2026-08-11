from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Complaint


@login_required
def dashboard(request):

    if request.user.is_staff:
        complaints = Complaint.objects.all().order_by('-created_at')

        total = complaints.count()

        pending = complaints.filter(
            status__in=['Submitted', 'Assigned']
        ).count()

        progress = complaints.filter(
            status='In Progress'
        ).count()

        resolved = complaints.filter(
            status__in=['Resolved', 'Closed']
        ).count()

        return render(
            request,
            'staff_dashboard.html',
            {
                'total': total,
                'pending': pending,
                'progress': progress,
                'resolved': resolved,
                'complaints': complaints,
            }
        )

    complaints = Complaint.objects.filter(
        user=request.user
    ).order_by('-created_at')

    total = complaints.count()

    pending = complaints.filter(
        status__in=['Submitted', 'Assigned']
    ).count()

    progress = complaints.filter(
        status='In Progress'
    ).count()

    resolved = complaints.filter(
        status__in=['Resolved', 'Closed']
    ).count()

    return render(
        request,
        'dashboard.html',
        {
            'total': total,
            'pending': pending,
            'progress': progress,
            'resolved': resolved,
        }
    )


@login_required
def create_complaint(request):

    if request.method == 'POST':

        Complaint.objects.create(
            user=request.user,
            category=request.POST.get('category'),
            location=request.POST.get('location'),
            description=request.POST.get('description'),
            priority=request.POST.get('priority'),
            image=request.FILES.get('image')
        )

        return redirect('/complaints/')

    return render(
        request,
        'complaint_form.html'
    )


@login_required
def my_complaints(request):

    complaints = Complaint.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(
        request,
        'my_complaints.html',
        {
            'complaints': complaints
        }
    )


@login_required
def edit_complaint(request, complaint_id):

    if not request.user.is_staff:
        return redirect('/')

    complaint = get_object_or_404(
        Complaint,
        id=complaint_id
    )

    staff_users = User.objects.filter(
        is_staff=True,
        is_active=True
    ).order_by('username')

    if request.method == 'POST':

        status = request.POST.get('status')

        if status:
            complaint.status = status

        staff_id = request.POST.get('assigned_staff')

        if staff_id:

            staff_member = get_object_or_404(
                User,
                id=staff_id,
                is_staff=True,
                is_active=True
            )

            complaint.assigned_staff = staff_member

            if complaint.status == 'Submitted':
                complaint.status = 'Assigned'

        else:
            complaint.assigned_staff = None

        complaint.save()

        return redirect('/')

    return render(
        request,
        'edit_complaint.html',
        {
            'complaint': complaint,
            'staff_users': staff_users,
        }
    )
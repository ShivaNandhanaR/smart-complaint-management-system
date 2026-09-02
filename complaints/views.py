from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import Complaint


# ============================================================
# REGISTER
# ============================================================

def register(request):

    if request.method == "POST":

        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        if not username or not email or not password:
            messages.error(request, "Please fill all required fields.")
            return render(request, "register.html")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, "register.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, "register.html")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, "register.html")

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(
            request,
            "Account created successfully. Please login."
        )

        return redirect("login")

    return render(request, "register.html")


# ============================================================
# LOGIN
# ============================================================

def login_view(request):

    if request.user.is_authenticated:

        if request.user.is_staff:
            return redirect("staff_dashboard")

        return redirect("dashboard")

    if request.method == "POST":

        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        if not username or not password:

            messages.error(
                request,
                "Please enter username and password."
            )

            return render(request, "login.html")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            if user.is_staff:
                return redirect("staff_dashboard")

            return redirect("dashboard")

        messages.error(
            request,
            "Invalid username or password."
        )

    return render(request, "login.html")


# ============================================================
# LOGOUT
# ============================================================

def logout_view(request):

    logout(request)

    messages.success(
        request,
        "You have been logged out successfully."
    )

    return redirect("login")


# ============================================================
# USER DASHBOARD
# ============================================================

@login_required
def dashboard(request):

    # If staff opens the normal dashboard,
    # send them to the staff dashboard.
    if request.user.is_staff:
        return redirect("staff_dashboard")

    # Resident complaints only
    complaints = Complaint.objects.filter(
        user=request.user
    ).order_by("-created_at")

    total = complaints.count()

    pending = complaints.filter(
        status__iexact="Pending"
    ).count()

    progress = complaints.filter(
        status__iexact="In Progress"
    ).count()

    resolved = complaints.filter(
        status__iexact="Resolved"
    ).count()

    context = {
        "complaints": complaints,
        "total": total,
        "pending": pending,
        "progress": progress,
        "resolved": resolved,
    }

    return render(
        request,
        "dashboard.html",
        context
    )

# ============================================================
# CREATE COMPLAINT
# ============================================================

@login_required
def create_complaint(request):

    if request.method == "POST":

        category = request.POST.get("category", "").strip()
        location = request.POST.get("location", "").strip()
        description = request.POST.get("description", "").strip()
        priority = request.POST.get("priority", "Medium").strip()

        image = request.FILES.get("image")

        if not category or not location or not description:
            messages.error(
                request,
                "Please fill all required fields."
            )

            return render(
                request,
                "complaint_form.html"
            )

        Complaint.objects.create(
            user=request.user,
            category=category,
            location=location,
            description=description,
            image=image,
            priority=priority,
            status="Pending"
        )

        messages.success(
            request,
            "Complaint submitted successfully!"
        )

        return redirect("my_complaints")

    return render(
        request,
        "complaint_form.html"
    )

# ============================================================
# MY COMPLAINTS
# ============================================================

@login_required
def my_complaints(request):

    complaints = Complaint.objects.filter(
        user=request.user
    ).order_by("-created_at")

    context = {
        "complaints": complaints
    }

    return render(
        request,
        "my_complaints.html",
        context
    )


# ============================================================
# EDIT COMPLAINT
# ============================================================

@login_required
def edit_complaint(request, complaint_id):

    complaint = get_object_or_404(
        Complaint,
        id=complaint_id
    )

    # Only the complaint owner or staff can edit
    if not request.user.is_staff and complaint.user != request.user:
        messages.error(
            request,
            "You are not allowed to edit this complaint."
        )
        return redirect("my_complaints")

    # Staff list
    staff_users = User.objects.filter(
        is_staff=True
    )

    if request.method == "POST":

        complaint.category = request.POST.get(
            "category",
            complaint.category
        ).strip()

        complaint.location = request.POST.get(
            "location",
            complaint.location
        ).strip()

        complaint.description = request.POST.get(
            "description",
            complaint.description
        ).strip()

        complaint.priority = request.POST.get(
            "priority",
            complaint.priority
        ).strip()

        # Only staff can update status and assigned staff
        if request.user.is_staff:

            complaint.status = request.POST.get(
                "status",
                complaint.status
            ).strip()

            assigned_staff_id = request.POST.get(
                "assigned_staff"
            )

            if assigned_staff_id:
                complaint.assigned_staff_id = assigned_staff_id
            else:
                complaint.assigned_staff = None

        # Update image if a new one was selected
        if request.FILES.get("image"):
            complaint.image = request.FILES["image"]

        complaint.save()

        messages.success(
            request,
            "Complaint updated successfully!"
        )

        if request.user.is_staff:
            return redirect("staff_dashboard")

        return redirect("my_complaints")

    context = {
        "complaint": complaint,
        "staff_users": staff_users,
    }

    return render(
        request,
        "edit_complaint.html",
        context
    )

# ============================================================
# STAFF DASHBOARD
# ============================================================

@login_required
def staff_dashboard(request):

    if not request.user.is_staff:
        return redirect("dashboard")

    complaints = Complaint.objects.all().order_by(
        "-created_at"
    )

    total = complaints.count()

    pending = complaints.filter(
        status__iexact="Pending"
    ).count()

    progress = complaints.filter(
        status__iexact="In Progress"
    ).count()

    resolved = complaints.filter(
        status__iexact="Resolved"
    ).count()

    context = {
        "complaints": complaints,
        "total": total,
        "pending": pending,
        "progress": progress,
        "resolved": resolved,
    }

    return render(
        request,
        "staff_dashboard.html",
        context
    )
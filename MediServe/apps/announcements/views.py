

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from utils.supabase_client import supabase
from datetime import datetime
from .models import Announcement


# ------------------------------
# ADMIN: Manage Announcements
# ------------------------------

@login_required
def announcements_view(request):
    """Admin can view, add, edit, and delete announcements."""
    # ✅ Check admin access
    is_admin = request.user.is_staff or request.user.email == "admin123@gmail.com"

    if not is_admin:
        messages.error(request, "Access denied. Admins only.")
        return redirect('main_menu')

    # ✅ Add new announcement
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')

        if not title or not content:
            messages.error(request, "Please fill in all fields.")
            return redirect('announcements')

        supabase.table("tblannouncements").insert({
            "title": title,
            "content": content,
            "date_posted": datetime.now().isoformat()
        }).execute()

        messages.success(request, "Announcement posted successfully!")
        return redirect('announcements')

    # ✅ Fetch all announcements
    data = supabase.table("tblannouncements").select("*").order("date_posted", desc=True).execute()
    announcements = data.data if data.data else []

    return render(request, 'announcements.html', {
        'announcements': announcements,
        'is_admin': is_admin  # ✅ This flag enables Edit/Delete buttons
    })


# ------------------------------
# ADMIN: Edit an Announcement
# ------------------------------

@login_required
def edit_post(request, post_id):
    """Admin edits an existing announcement."""
    if not request.user.is_staff and request.user.email != "admin123@gmail.com":
        messages.error(request, "Unauthorized access.")
        return redirect("announcements")

    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")

        if not title or not content:
            messages.error(request, "Title and content are required.")
            return redirect("announcements")

        supabase.table("tblannouncements").update({
            "title": title,
            "content": content
        }).eq("id", post_id).execute()

        messages.success(request, "Announcement updated successfully.")
        return redirect("announcements")

    # ✅ Pre-fill form with existing data
    data = supabase.table("tblannouncements").select("*").eq("id", post_id).execute()
    if not data.data:
        messages.error(request, "Announcement not found.")
        return redirect("announcements")

    announcement = data.data[0]
    return render(request, "edit_announcement.html", {"announcement": announcement})


# ------------------------------
# ADMIN: Delete an Announcement
# ------------------------------

@login_required
def delete_post(request, post_id):
    """Admin deletes an announcement."""
    if not request.user.is_staff and request.user.email != "admin123@gmail.com":
        messages.error(request, "Unauthorized access.")
        return redirect("announcements")

    supabase.table("tblannouncements").delete().eq("id", post_id).execute()
    messages.success(request, "Announcement deleted successfully.")
    return redirect("announcements")


# ------------------------------
# USER: View Announcements
# ------------------------------

@login_required
def view_announcements(request):
    """Users view all posted announcements."""
    data = supabase.table("tblannouncements").select("*").order("date_posted", desc=True).execute()
    announcements = data.data if data.data else []
    return render(request, "view_announcements.html", {"announcements": announcements})

@login_required
def add_post(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")

        # Save announcement
        Announcement.objects.create(title=title, content=content)
        return redirect('announcements')  # or whatever your main announcements page is named

    return render(request, 'add_post.html')  # optional if you want a standalone page
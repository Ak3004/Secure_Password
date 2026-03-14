from django.shortcuts import redirect, render
from django.urls import reverse

from .password import (
    authenticate,
    add_password_entry,
    delete_password_entry,
    get_password_entry,
    get_user_passwords,
    update_password_entry,
)


def _get_logged_in_uid(request):
    """Return the uid stored in the session, or None."""
    return request.session.get('uid')


def login_view(request):
    """Simple login page that stores uid in session if authenticated."""
    error = None
    if request.method == 'POST':
        uid = request.POST.get('uid')
        password = request.POST.get('password')
        if not uid or not password:
            error = 'UID and password are required.'
        elif not authenticate(uid, password):
            error = 'Invalid credentials.'
        else:
            request.session['uid'] = uid
            return redirect(reverse('main-dashboard'))

    return render(request, 'main/login.html', {'error': error})


def logout_view(request):
    request.session.pop('uid', None)
    return redirect(reverse('main-login'))


def dashboard_view(request):
    """Dashboard for managing password entries (requires login)."""
    uid = _get_logged_in_uid(request)
    if not uid:
        return redirect(reverse('main-login'))

    message = None
    entries = get_user_passwords(uid)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
            domain = request.POST.get('domain')
            pwd = request.POST.get('pwd')
            if not domain:
                message = 'Domain is required to add a password.'
            else:
                add_password_entry(uid, domain, pwd)
                message = f'Added password for {domain}.'
                entries = get_user_passwords(uid)
        elif action == 'update':
            idx = int(request.POST.get('index', -1))
            new_pwd = request.POST.get('pwd')
            if idx < 0:
                message = 'Invalid index.'
            else:
                updated = update_password_entry(uid, idx, new_pwd)
                if updated is None:
                    message = 'Entry not found.'
                else:
                    message = f'Updated password for {updated["domain"]}.'
                    entries = get_user_passwords(uid)
        elif action == 'delete':
            idx = int(request.POST.get('index', -1))
            if idx < 0:
                message = 'Invalid index.'
            else:
                deleted = delete_password_entry(uid, idx)
                if deleted is None:
                    message = 'Entry not found.'
                else:
                    message = f'Deleted password for {deleted["domain"]}.'
                    entries = get_user_passwords(uid)

    return render(
        request,
        'main/dashboard.html',
        {'uid': uid, 'entries': entries, 'message': message},
    )

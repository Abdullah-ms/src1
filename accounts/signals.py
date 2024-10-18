from django.contrib.auth.signals import user_logged_in
from django.contrib.sessions.models import Session
from django.utils.timezone import now
from django.contrib import messages


def terminate_other_sessions(sender, user, request, **kwargs):
    sessions = Session.objects.filter(expire_date__gte=now())
    for session in sessions:
        data = session.get_decoded()
        if data.get('_auth_user_id') == str(user.id):
            if session.session_key != request.session.session_key:
                session.delete()
                request.session['session_terminated'] = True


user_logged_in.connect(terminate_other_sessions)

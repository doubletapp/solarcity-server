from django.conf.urls import url
from django.urls import include

from api.auth.views import LoginView, SignupView, ChangePasswordView, SendResetPasswordEmailView, ResetPasswordView
from api.chat.views import PostMessageView, HistoryView
from api.views import PostReportView, ReportsHistoryView


urlpatterns = [
    url(r'^login/', LoginView.as_view()),
    url(r'^signup/', SignupView.as_view()),
    url(r'^change_password/', ChangePasswordView.as_view()),
    url(r'^send_reset_password_email/', SendResetPasswordEmailView.as_view()),
    url(r'^reset_password/', ResetPasswordView.as_view()),
    url(r'^chat/post/', PostMessageView.as_view()),
    url(r'^chat/history/', HistoryView.as_view()),
    url(r'^report/post/', PostReportView.as_view()),
    url(r'^report/history/', ReportsHistoryView.as_view()),
]

from __future__ import annotations

import typing

from allauth.account.adapter import DefaultAccountAdapter
# from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from django.http import HttpRequest
from allauth.account.utils import filter_users_by_email


if typing.TYPE_CHECKING:
    # from allauth.socialaccount.models import SocialLogin
    from cvback.users.models import User


class NoMsg:

    def send(self):
        print("NOSEND")


class AccountAdapter(DefaultAccountAdapter):

        
    def is_open_for_signup(self, request: HttpRequest) -> bool:
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)
    
    def render_mail(self, template_prefix, email, context, headers=None):
        users = filter_users_by_email(email,is_active=True, prefer_verified=True)
        if not users and "/_allauth/browser/v1/auth/password/request" == context["request"].path:
            return NoMsg()
        if template_prefix == "account/email/password_reset_key":
            context["password_reset_url"] = context["password_reset_url"].replace("/accounts/", "/#/account/") 
            print(context)
        return super().render_mail(template_prefix,email,context,headers=headers)

    def send_mail_(self, template_prefix, email, context,request):
        ctx = {
            "email": email,            
            "current_site": request,
            
        }
        ctx.update(context)
        msg = super().render_mail(template_prefix, email, ctx)
        #msg.attach(context["filename"],context["file"],context["mime_type"])
        msg.send()

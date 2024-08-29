from __future__ import annotations

import typing

from allauth.account.adapter import DefaultAccountAdapter
# from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from django.http import HttpRequest


from allauth.account.forms import ResetPasswordForm
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
        print(context["request"].path)
        if not users and "/_allauth/browser/v1/auth/password/request" == context["request"].path:
            return NoMsg()
        if template_prefix == "account/email/password_reset_key":
            context["password_reset_url"] = context["password_reset_url"].replace("/accounts/", "/#/account/") 
        return super().render_mail(template_prefix,email,context,headers=headers)

    def send_mail(self, template_prefix, email, context,request ):
        ctx = {
            "email": email,
            "current_site": "",
            
        }
        ctx.update(context)
        msg = super().render_mail(template_prefix, email, ctx)
        msg.send()
        
# class SocialAccountAdapter(DefaultSocialAccountAdapter):
#     def is_open_for_signup(self, request: HttpRequest, sociallogin: SocialLogin) -> bool:
#         return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)
#
#     def populate_user(self, request: HttpRequest, sociallogin: SocialLogin, data: dict[str, typing.Any]) -> User:
#         """
#         Populates user information from social provider info.
#
#         See: https://django-allauth.readthedocs.io/en/latest/advanced.html?#creating-and-populating-user-instances
#         """
#         user = sociallogin.user
#         if name := data.get("name"):
#             user.name = name
#         elif first_name := data.get("first_name"):
#             user.name = first_name
#             if last_name := data.get("last_name"):
#                 user.name += f" {last_name}"
#         return super().populate_user(request, sociallogin, data)

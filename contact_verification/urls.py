from django.urls import path

from contact_verification.views import (
    ContactVerificationViewSet,
    CodeVerificationViewSet,
)

contact_verification = ContactVerificationViewSet.as_view({"post": "create"})
email_verification = CodeVerificationViewSet.as_view({"post": "verify_email"})
phone_verification = CodeVerificationViewSet.as_view({"post": "verify_phone"})


urlpatterns = [
    path("email_the_code/", contact_verification, name="contact-verification"),
    path("verify_email/", email_verification, name="email-verification"),
    path("verify_phone/", phone_verification, name="phone-verification"),
]

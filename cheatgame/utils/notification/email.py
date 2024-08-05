from django.core.mail import send_mail


def send_verification_code(otp: str, email: str) -> None:
    subject = f'Verify Email'
    message = {f'Wellcome to Cheats game\n'
               f'your verification code is:{otp} '}
    from_email = "send from this email"
    recipient_list = [email , ]
    send_mail(subject ,message , from_email ,recipient_list ,fail_silently=True)


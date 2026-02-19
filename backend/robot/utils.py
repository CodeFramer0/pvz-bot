import random
import string

from django.conf import settings
from django.core.mail import EmailMultiAlternatives, send_mail


def generate_numeric_code(length=6):
    return "".join(random.choices(string.digits, k=length))


def send_verification_email(email: str, code: str, html: str = None):
    subject = "Код подтверждения"
    from_email = settings.DEFAULT_FROM_EMAIL
    to = [email]

    # plain text fallback
    text_content = f"Ваш код подтверждения: {code}\nДействует 5 минут."

    # если html передан, используем его, иначе формируем стандартное письмо
    if html is None:
        html_content = f"""
        <html>
          <body style="font-family: Arial, sans-serif; background-color: #f5f5f5; padding: 20px;">
            <div style="max-width: 600px; margin: auto; background-color: #ffffff; padding: 30px; border-radius: 8px; text-align: center;">
              <h2 style="color: #333;">Подтверждение Email</h2>
              <p style="font-size: 16px; color: #555;">Ваш код подтверждения:</p>
              <div style="margin: 20px 0; font-size: 32px; font-weight: bold; color: #1a73e8; letter-spacing: 4px;">{code}</div>
              <p style="font-size: 14px; color: #777;">Код действителен 5 минут.</p>
              <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
              <p style="font-size: 12px; color: #aaa;">Если вы не отправляли этот запрос, просто проигнорируйте это письмо.</p>
            </div>
          </body>
        </html>
        """
    else:
        # если html пришёл извне, просто вставляем в письмо
        html_content = html

    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send(fail_silently=False)
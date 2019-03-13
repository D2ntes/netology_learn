# -*- coding: utf-8 -*-
# Домашнее задание к лекции 1.5 «Zen of Python - что должен знать каждый разработчик / PEP8 и PEP»

# * Мы устроились на новую работу. Бывший сотрудник начал разрабатывать модуль для работы с почтой, но не успел доделать его. Код рабочий. Нужно только провести рефакторинг кода.
#
# 1. Создать класс для работы с почтой;
# 2. Создать методы для отправки и получения писем;
# 3. Убрать "захардкоженный" код. Все значения должны определяться как аттрибуты класса, либо аргументы методов;
# 4. Переменные должны быть названы по стандарту PEP8;
# 5. Весь остальной код должен соответствовать стандарту PEP8;
# 6. Класс должен инициализироваться в конструкции.
# if __name__ == '__main__'
# Скрипт для работы с почтой.
#
# import email
# import smtplib
# import imaplib
# from email.MIMEText import MIMEText
# from email.MIMEMultipart import MIMEMultipart
#
#
# GMAIL_SMTP = "smtp.gmail.com"
# GMAIL_IMAP = "imap.gmail.com"
#
# l = 'login@gmail.com'
# passwORD = 'qwerty'
# subject = 'Subject'
# recipients = ['vasya@email.com', 'petya@email.com']
# message = 'Message'
# header = None
#
#
# #send message
# msg = MIMEMultipart()
# msg['From'] = l
# msg['To'] = ', '.join(recipients)
# msg['Subject'] = subject
# msg.attach(MIMEText(message))
#
# ms = smtplib.SMTP(GMAIL_SMTP, 587)
# # identify ourselves to smtp gmail client
# ms.ehlo()
# # secure our email with tls encryption
# ms.starttls()
# # re-identify ourselves as an encrypted connection
# ms.ehlo()
#
# ms.login(l, passwORD)
# ms.sendmail(l,
# ms, msg.as_string())
#
# ms.quit()
# #send end
#
#
# #recieve
# mail = imaplib.IMAP4_SSL(GMAIL_IMAP)
# mail.login(l, passwORD)
# mail.list()
# mail.select("inbox")
# criterion = '(HEADER Subject "%s")' % header if header else 'ALL'
# result, data = mail.uid('search', None, criterion)
# assert data[0], 'There are no letters with current header'
# latest_email_uid = data[0].split()[-1]
# result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
# raw_email = data[0][1]
# email_message = email.message_from_string(raw_email)
# mail.logout()
# #end receive

import email
import imaplib
import smtplib

DEFAULT_SMTP = 'smtp.mail.ru'
DEFAULT_IMAP = 'imap.mail.ru'


class MailBox:
    letters_current_header = 0
    last_letter = -1
    raw_mail = 1

    def __init__(self, login, password, email_smtp=DEFAULT_SMTP, email_iap=DEFAULT_IMAP, **kwargs):
        self.login = login
        self.password = password
        self.mail_server_smtp = smtplib.SMTP(email_smtp, 587)
        self.mail_server_iap = imaplib.IMAP4_SSL(email_iap)

    def send_mail(self, subject, recipients, message=''):
        # the formation of the body of the email
        letter = email.message.EmailMessage()
        letter['From'] = self.login
        letter['To'] = ', '.join(recipients)
        letter['Subject'] = subject
        letter.set_content(message)

        self.mail_server_smtp.ehlo()  # identify ourselves to smtp mail.ru client
        self.mail_server_smtp.starttls()  # secure our email with tls encryption
        self.mail_server_smtp.ehlo()  # re-identify ourselves as an encrypted connection
        self.mail_server_smtp.login(self.login, self.password)
        self.mail_server_smtp.sendmail(self.login, recipients, letter.as_bytes())
        self.mail_server_smtp.quit()

    def receive_mail(self, allowed_header):
        self.mail_server_iap.login(self.login, self.password)
        self.mail_server_iap.select("inbox")

        allowed_header = allowed_header if allowed_header is not None else "ALL"
        criterion = f'{allowed_header}'

        _, received_letters = self.mail_server_iap.uid('search', None, criterion)
        assert received_letters[self.letters_current_header], 'There are no letters with current header'

        latest_email_uid = received_letters[self.letters_current_header].split()[self.last_letter]
        _, received_letters = self.mail_server_iap.uid('fetch', latest_email_uid, '(RFC822)')

        raw_email = received_letters[self.letters_current_header][self.raw_mail]
        email_message = email.message_from_bytes(raw_email)

        self.mail_server_iap.logout()
        return email_message


if __name__ == '__main__':
    # settings for identification & authentication
    mail_login = ''
    mail_password = ''

    # properties of the sent message
    mail_subject = 'Test'
    mail_recipients = ['', '']
    mail_message = 'Netology ADPY-2'

    # criterion for search letter
    mail_header = None

    mail_box = MailBox(login=mail_login, password=mail_password)
    mail_box.send_mail(subject=mail_subject, recipients=mail_recipients, message=mail_message)
    print(mail_box.receive_mail(allowed_header=mail_header))

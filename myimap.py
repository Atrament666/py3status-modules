# -*- coding: utf-8 -*-
"""
Display number of unread messages from IMAP account.

Configuration parameters:
    allow_urgent: display urgency on unread messages (default False)
    cache_timeout: refresh interval for this module (default 60)
    criterion: status of emails to check for (default 'UNSEEN')
    format: display format for this module (default 'Mail: {unseen}')
    hide_if_zero: hide this module when no new mail (default False)
    mailbox: name of the mailbox to check (default 'INBOX')
    password: login password (default None)
    password_file: path to a file containing gpg encrypted password (default None)
    port: number to use (default '993')
    security: login authentication method: 'ssl' or 'starttls'
        (startssl needs python 3.2 or later) (default 'ssl')
    server: server to connect (default None)
    user: login user (default None)

Format placeholders:
    {unseen} number of unread emails

Color options:
    color_new_mail: use color when new mail arrives, default to color_good

@author obb, gpg suport added by Atrament

SAMPLE OUTPUT
{'full_text': 'Mail: 36', 'color': '#00FF00'}
"""
import imaplib
import gnupg
from ssl import create_default_context
STRING_UNAVAILABLE = 'N/A'


class Py3status:
    """
    """
    # available configuration parameters
    allow_urgent = False
    cache_timeout = 60
    criterion = 'UNSEEN'
    format = 'Mail: {unseen}'
    hide_if_zero = False
    mailbox = 'INBOX'
    password = None
    password_file = None
    port = '993'
    security = 'ssl'
    server = None
    user = None

    class Meta:
        deprecated = {
            'rename': [
                {
                    'param': 'new_mail_color',
                    'new': 'color_new_mail',
                    'msg': 'obsolete parameter use `color_new_mail`',
                },
                {
                    'param': 'imap_server',
                    'new': 'server',
                    'msg': 'obsolete parameter use `server`',
                },
            ],
        }

    def post_config_hook(self):
        if self.security not in ["ssl", "starttls"]:
            raise ValueError("Unknown security protocol")

    def check_mail(self):

        mail_count = self._get_mail_count()

        response = {'cached_until': self.py3.time_in(self.cache_timeout)}

        if mail_count is None:
            response['color'] = self.py3.COLOR_BAD,
            response['full_text'] = self.py3.safe_format(
                self.format, {'unseen': STRING_UNAVAILABLE})
        elif mail_count > 0:
            response['color'] = self.py3.COLOR_NEW_MAIL or self.py3.COLOR_GOOD
            if self.allow_urgent:
                response['urgent'] = True

        if mail_count == 0 and self.hide_if_zero:
            response['full_text'] = ''
        else:
            response['full_text'] = self.py3.safe_format(
                self.format, {'unseen': mail_count})

        return response

    def _connection_ssl(self):
        print(f'Connecting to: {self.server} port: {self.port}')
        connection = imaplib.IMAP4_SSL(self.server, self.port)
        return connection

    def _connection_starttls(self):
        connection = imaplib.IMAP4(self.server, self.port)
        connection.starttls(create_default_context())
        return connection

    def _get_mail_count(self):
        try:
            mail_count = 0
            directories = self.mailbox.split(',')

            if self.security == "ssl":
                connection = self._connection_ssl()
            elif self.security == "starttls":
                connection = self._connection_starttls()


            if not self.password and self.password_file:
                with open(self.password_file, 'r') as file:
                    self.password = file.readline()

# this part is commented because the new gnupg version doesn't work with python 3, so we need to read the password directly
#            if not self.password and self.password_file:
#                gpg = gnupg.GPG()
#                with open(self.password_file,'rb') as f:
#                    self.password =str(gpg.decrypt_file(f)).rstrip()

            connection.login(self.user, self.password)

            for directory in directories:
                connection.select(directory)
                unseen_response = connection.search(None, self.criterion)
                mails = unseen_response[1][0].split()
                mail_count += len(mails)

            connection.close()
            return mail_count
        except:
            return None


if __name__ == "__main__":
    """
    Run module in test mode.
    """
    from py3status.module_test import module_test
    Py3status.password_file='/home/atrament/.i3/imap_password'
    Py3status.user='atramenent666'
    Py3status.server='imap.gmail.com'
    Py3status.port='993'
    module_test(Py3status)

# encoding: utf-8

import os
import sys
from email.utils import formataddr

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import argparse
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from jinja2 import Environment
from jinja2 import PackageLoader

from mailer.config import SENDER, PWD, SERVER, PORT, TLS, DEST_BURO, DEST_CA, USERNAME

env = Environment(loader=PackageLoader('mailer'))


class CR:
    def __init__(self, url):
        self.url = url

    @property
    def team(self):
        if 'ca' in self.url.lower():
            return 'CA'
        elif 'bureau' in self.url.lower():
            return 'Buro'
        else:
            return ''

    @property
    def date(self):
        return '/'.join(self._date())

    def _date(self):
        filename = self.url.split('/')[-1]
        date = filename.split('_', maxsplit=3)
        del(date[3])
        return reversed(date)

    @property
    def short_date(self):
        date = list(self._date())
        del(date[2])
        return '/'.join(date)

    def __str__(self):
        return self.url


def send_mail(server, msg, dst, cr_list):
    template = env.get_template('mail-template.html')
    content = template.render(cr_list=cr_list)
    msg['To'] = dst
    msg['Subject'] = 'CR {0} pour validation'.format(', '.join(map(lambda x: x.short_date, cr_list)))
    msg.attach(MIMEText(content, 'html'))
    server.sendmail(SENDER, msg['To'], msg.as_string())


def main(urls):
    cr_list = map(CR, urls)
    cr_ca = []
    cr_buro = []

    for cr in cr_list:
        if cr.team == 'CA':
            cr_ca.append(cr)
        elif cr.team == 'Buro':
            cr_buro.append(cr)

    server = smtplib.SMTP(SERVER, PORT)
    if TLS:
        server.starttls()
    server.login(USERNAME, PWD)

    msg = MIMEMultipart('alternative')
    msg['From'] = formataddr(('Secrétaire Général', SENDER))

    if len(cr_ca) > 0:
        send_mail(server, msg, DEST_CA, cr_ca)

    if len(cr_buro) > 0:
        send_mail(server, msg, DEST_BURO, cr_buro)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-u', '--urls', type=str, nargs='+', help='CR URLs to send.', required=True)

    args = ap.parse_args()
    urls = args.urls

    main(urls)

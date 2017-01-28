#!/usr/bin/env python
# coding=utf-8

import random
import uuid
import datetime

log_size = 10000

# Create a list of unique ID
id_list = []
size_list = log_size + 1
while size_list > 0:
    tmp = str(uuid.uuid1()).replace('-', '')[0:10].upper()
    id_list.append(tmp)
    size_list = size_list - 1
id_list = list(set(id_list))

skel_item = [
    [
        "{{TIME_TIME}} srv-mailing1 postfix/qmgr[2813]: {{IDIDID}}: "
        "from=<{{MAIL_FROM}}>, size=1205, nrcpt=1 (queue active)",
        "{{TIME_TIME}} srv-mailing1 postfix/smtp[4434]: {{IDIDID}}: "
        "to=<{{MAIL_TO}}>, relay=relay.smtp.lambda[12.123.123.125]:25, "
        "delay=0.23, delays=0.15/0/0.03/0.05, dsn=2.0.0, status=sent "
        "(250 2.0.0 OK 1447737909 18si30718365wmg.112 - gsmtp)"
    ],
    [
        "{{TIME_TIME}} srv-mailing1 postfix/qmgr[2813]: {{IDIDID}}: "
        "from=<{{MAIL_FROM}}>, size=8480, nrcpt=1 (queue active)",
        "{{TIME_TIME}} srv-mailing1 postfix/smtp[4446]: {{IDIDID}}: "
        "to=<{{MAIL_TO}}>, relay=relay.smtp.lambda[12.123.123.125]:25, "
        "delay=0.08, delays=0.04/0/0/0.03, dsn=2.0.0, status=sent "
        "(250 2.0.0 Ok: queued as {{IDIDID}})"
    ],
    [
        "{{TIME_TIME}} srv-mailing1 postfix/qmgr[2813]: {{IDIDID}}: "
        "from=<>, size=965, nrcpt=1 (queue active)",
        "{{TIME_TIME}} srv-mailing1 postfix/smtp[4432]: {{IDIDID}}: "
        "to=<{{MAIL_TO}}>, relay=none, delay=0.04, delays=0.04/0/0/0,"
        " dsn=5.4.4, status=bounced (Host or domain name not found. "
        "Name service error for name=toto_www1 type=A: Host not found)"
    ],
    [
        "{{TIME_TIME}} srv-mailing1 postfix/qmgr[2813]: {{IDIDID}}: "
        "from=<{{MAIL_FROM}}>, size=4476, nrcpt=1 (queue active)",
        "{{TIME_TIME}} srv-mailing1 postfix/smtp[4442]: {{IDIDID}}: "
        "to=<{{MAIL_TO}}>, relay=relay.smtp.lambda[12.123.123.125]:25, "
        "delay=0.45, delays=0.08/0/0.26/0.1, dsn=5.1.1, status=bounced "
        "(host alt1.aspmx.l.google.com[74.125.205.26] said: 550-5.1.1 The "
        "email account that you tried to reach does not exist. Please try "
        "550-5.1.1 double-checking the recipient's email address for typos or "
        "550-5.1.1 unnecessary spaces. Learn more at 550 5.1.1  "
        "https://support.google.com/mail/answer/6596 us19si29356293lbb.45 - "
        "gsmtp (in reply to RCPT TO command))"]
]

mail_address = [
    "foreignexchangedept1@yahoo.com.hk",
    "williamsgeorgeatmcarddept1@gmail.com",
    "ericlim220@yahoo.com",
    "mr.paul.harry08@gmail.com",
    "katblix4@gmail.com",
    "felica4uu@hotmail.com",
    "j.nomvete30@workmail.co.za",
    "paul_ku2@hotmail.com",
    "davis_mark1@outlook.com",
    "sgtamyrhodes@qq.com",
    "dhldelivery@pochta.com",
    "arfinances@live.com",
    "help202@outlook.dk",
    "mrs.gloriamackenie@outlook.com",
    "shand_lee@yahoo.com.hk",
    "franklinosayandescott@gmail.com",
    "pmark5193@gmail.com",
    "westernunion1233@yahoo.fr",
    "iwumt2015@gmail.com",
    "mathewgdfoundation@qq.com",
    "johnpaulpatrick_77@hotmail.com",
    "davidmike_201@yahoo.co.jp",
    "detailsunitednations@gmail.com",
    "newgovernorcbn2014@gmail.com",
    "gordch101@yahoo.com.hk",
    "Petersimonsbacka@swedishmedtech.se.com",
    "dipjsc.dubai@gmail.com",
    "dipjsc.uae@gmail.com",
    "qrtinfoyou@gmail.com",
    "executive.jalloh@gmail.com",
    "unsubemail55@gmail.com",
    "cpiatbariloche@speedy.com.ar",
    "manitoba02@gmail.com",
    "dr.robertp1@hotmail.com",
    "western.union577@qq.com",
    "upsservices9201@outlook.com",
    "mr.jamescornwall@qq.com",
    "frankcartercashflowinvestment@yahoo.com",
    "carlzeichner@email.ch",
    "barristeronyelilian5@gmail.com",
    "mr.paulconnick@hotmail.com",
    "firstbankplcng@accountant.com",
    "mrbenraymond1957@gmx.com",
    "t.pbena1@foxmail.com",
    "ggregor932@gmail.com",
    "america-seafood@hotmail.com",
    "aandmengineering@msn.com",
    "info@maerskoilgroup.com",
    "mrsjanetyellen3@gmail.com",
    "andreidmitrievbulkserver@gmail.com",
    "ousmansoumah003@gmail.com",
    "kushi.alltoit@hotmail.com",
    "addaieric002@gmail.com",
    "moneygram08@foxmail.com",
    "foreignpaymentdepartment@lycos.com",
    "musolinofinancefinco@gmail.com",
    "2724479582@qq.com",
    "inf0@pisem.net",
    "adom-thiemele@thiemele-lawfirm.com",
    "hgbfcf9@hotmail.com",
    "serline_klein@hotmail.com",
    "kindlyremove008@gmail.com",
    "mr.andrew_pedro@yahoo.fr",
    "mr.andrew_pedro@yahoo.fr",
    "newlook2k8.bye@gmail.com",
    "cmfinancialservices07@gmail.com",
    "CameronDokodaFinancialServices@consultant.com",
    "tfgiftinvestment2@gmail.com",
    "moneytransferwesternunion75@yahoo.com.vn",
    "leon.hirtle2@hotmail.com",
    "slaveigood1@gmail.com",
    "paull.bben@gmail.com",
    "western.u844@mail.ru",
    "lottowinnerrewards@gmail.com",
    "david.ellis01@outlook.com",
    "raymond.buxton2015@hotmail.com",
    "kw648@yahoo.com.hk",
    "InfoNedbank.Nedbank@yahoo.co.za",
    "minkolwi@gmail.com",
    "inamullahkhan627@gmail.com",
    "foreign.transfer_paymen.dpt@financier.com",
    "transferdepartment.b@accountant.com"
]

tmp_date = 'Nov 17 06:25:21'
year = 2015
month = tmp_date.split(' ')[0]
day = tmp_date.split(' ')[1]
time = tmp_date.split(' ')[2]
tmpyear = '%s %s %s %s' % (year,
                           month,
                           day,
                           time)
base = datetime.datetime.strptime(tmpyear, '%Y %b %d %H:%M:%S')


def make_mail_log():
    global skel_item
    global mail_address
    global log_size
    global id_list
    global base

    tmp_skel_from = random.choice(skel_item)[0]
    tmp_skel_to = random.choice(skel_item)[1]
    tmp_mail_from = random.choice(mail_address)
    tmp_mail_to = random.choice(mail_address)
    tmp_id = id_list[log_size]
    tmp_date = base.strftime('%b %d %H:%M:%S')
    base = base + datetime.timedelta(seconds=random.randint(2, 20))

    tmp_skel_from = tmp_skel_from.replace('{{TIME_TIME}}', tmp_date)
    tmp_date = base.strftime('%b %d %H:%M:%S')
    base = base + datetime.timedelta(seconds=random.randint(2, 20))
    tmp_skel_to = tmp_skel_to.replace('{{TIME_TIME}}', tmp_date)
    tmp_skel_from = tmp_skel_from.replace('{{MAIL_FROM}}', tmp_mail_from)
    tmp_skel_to = tmp_skel_to.replace('{{MAIL_TO}}', tmp_mail_to)
    tmp_skel_from = tmp_skel_from.replace('{{IDIDID}}', tmp_id)
    tmp_skel_to = tmp_skel_to.replace('{{IDIDID}}', tmp_id)

    return (tmp_skel_from, tmp_skel_to)


def create_log_file():
    global log_size

    fd = open('mail.log.gen', 'w+')

    while log_size > 0:
        var1, var2 = make_mail_log()
        fd.write(var1+'\n')
        fd.write(var2+'\n')
        log_size = log_size - 1

create_log_file()

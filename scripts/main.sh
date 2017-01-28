#!/usr/bin/env bash

param=$@

echo $param

printf '\nSERVER 2\n'
ssh localhost "python /root/log/check_mail.py $param"

printf '\nSERVER 3\n'
ssh localhost "python /root/log/check_mail.py $param"

printf '\nSERVER 4\n'
ssh localhost "python /root/log/check_mail.py $param"


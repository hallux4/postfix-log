#!/usr/bin/env bash

rm -rf check_mail check_mail.zip
mkdir app
cp __main__.py OrderedDict2.py app/
cd app
zip -r ../check_mail.zip *
cd ..
echo '#!/usr/bin/env python' | cat - check_mail.zip > check_mail
rm -rf app/ OrderedDict2.pyc
chmod +x check_mail

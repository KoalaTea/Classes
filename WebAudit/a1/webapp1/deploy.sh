#!/bin/bash

cp -f -R static /var/www/html
cp -f -R templates /var/www/cgi-bin
cp -f *.php /var/www/cgi-bin
chmod -R +x /var/www/cgi-bin

#!/bin/ash
kill $(ps aux | grep '[r]equests_mail.sh' | awk '{print $1}')
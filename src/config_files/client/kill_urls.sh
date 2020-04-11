#!/bin/ash
kill $(ps aux | grep '[r]equests_urls.sh' | awk '{print $1}')
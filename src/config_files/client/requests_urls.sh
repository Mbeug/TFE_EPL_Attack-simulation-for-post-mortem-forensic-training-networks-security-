#!/bin/ash
if [ $# != 3 ]; then
    echo "Please enter arguments [Min secondes] [Max secondes] [File with urls]"
    echo "Example: requests_urls.sh 2 5 url.txt"
    exit 0
fi
echo "Wait between $1 and $2 s"
echo "Url from $3"
while :
do
        echo "Sending request"
        wget -q -r $(shuf -n 1 $3) -O /tmp/my_temp
        sleep $(( ( RANDOM % $2 )  + $1 ))
done
#!/bin/ash
if [ $# != 5 ]; then
    echo "Please enter arguments [Min secondes] [Max secondes] [Sender] [Pass sender] [Receiver]"
    echo "Example: requests_mail.sh 2 5 bob alice max"
    exit 0
fi
echo "Wait between $1 and $2 s"
echo "From $3 to $5"
while :
do
        echo "Sending request"
        sed -e "s/\${sender}/$3/g" -e "s/\${receiver}/$5/g" -e "s/\${date}/$(date)/g" template_mail.txt > email.txt
        curl smtp://mail.local --mail-from $3@mail.local --mail-rcpt $5@mail.local --upload-file email.txt
        sleep $(( ( RANDOM % $2 )  + $1 ))
        curl --insecure --url "imaps://mail.local/" --user "$3:$4" -X 'EXAMINE INBOX'
        sleep $(( ( RANDOM % $2 )  + $1 ))
        curl --insecure --url "imaps://mail.local/" --user "$3:$4" -X 'STATUS INBOX (MESSAGES)' > inbox_status
        if grep -q "(MESSAGES 0)" "inbox_status"; then
            echo "No messages INBOX"
        else
            curl --insecure --url "imaps://mail.local/INBOX" --user "$3:$4" -X 'FETCH 1 BODY[]'
            sleep $(( ( RANDOM % $2 )  + $1 ))
            curl --insecure --url "imaps://mail.local/INBOX" --user "$3:$4" -X 'FETCH 1:* Flags'
            sleep $(( ( RANDOM % $2 )  + $1 ))
            curl --insecure --url "imaps://mail.local/INBOX" --user "$3:$4" -X 'STORE 1 +FLAGS \Deleted'
            sleep $(( ( RANDOM % $2 )  + $1 ))
            curl --insecure --url "imaps://mail.local/INBOX" --user "$3:$4" -X 'EXPUNGE'
            sleep $(( ( RANDOM % $2 )  + $1 ))
        fi
done
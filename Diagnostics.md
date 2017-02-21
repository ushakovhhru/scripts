List of ESTABLISHED TCP connections grouped by remote host name:

    netstat --numeric-ports -aT | grep -F ESTAB | sort -k 5 | awk '{print $5}' | sed 's/^\(.*\):[0-9]\+$/\1/' | uniq -c

List of ESTABLISHED TCP connections grouped by remote host name:

```bash
netstat --numeric-ports -aT | grep -F ESTAB | sort -k 5 | awk '{print $5}' | sed 's/^\(.*\):[0-9]\+$/\1/' | uniq -c
```

List of ESTABLISHED TCP connections grouped by connection owner process:

```bash
#!/bin/bash
me=$(basename $0)
snapshot=$(mktemp /tmp/$me-netstat-snapshot.XXXXXX)
exec 3>$snapshot
snapshotfd=/proc/$$/fd/3
rm $snapshot

netstat --numeric-ports -aTp 2>/dev/null | grep -F ESTABLISHED >&3

cat <$snapshotfd | awk '{print $7}' | sed 's:^\([0-9]\+\)/.*$:\1:' | sort -n | uniq -c | while read conns pid; do
        if [ "$pid" = "-" ]; then
                cmd="<kernel>"
                pidexpr=' -[ \t]*$'
        else
                cmd=$(ps -ww -p $pid --no-headers -o args)
                if [[ $cmd == *" -jar "* ]]; then
                        cmd=$(echo $cmd | sed 's:^.* -jar \([^ ]\+\).*$:\1:')
                fi
                pidexpr=" $pid/"
        fi
        printf "%-8d  %s\n" "$conns" "$cmd"
        cat <$snapshotfd | grep -- "$pidexpr" | sort -k 5 | awk '{print $5}' | sed 's/^\(.*\):[0-9]\+$/\1/' | uniq -c | while read subconns remote; do
                printf "    %-8d  %s\n" "$subconns" "$remote"
        done
done
```

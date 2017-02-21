List of ESTABLISHED TCP connections grouped by remote host name:

```bash
netstat --numeric-ports -aT | grep -F ESTAB | sort -k 5 | awk '{print $5}' | sed 's/^\(.*\):[0-9]\+$/\1/' | uniq -c
```

List of ESTABLISHED TCP connections grouped by connection owner process:

```bash
#!/bin/bash
netstat --numeric-ports -aTp 2>/dev/null | grep -F ESTAB | awk '{print $7}' | sed 's:^\([0-9]\+\)/.*$:\1:' | sort -n | uniq -c | while read conns pid; do
        if [ "$pid" = "-" ]; then
                cmd="<kernel>"
        else
                cmd=$(ps -ww -p $pid --no-headers -o args)
                if [[ $cmd == *" -jar "* ]]; then
                        cmd=$(echo $cmd | sed 's:^.* -jar \([^ ]\+\).*$:\1:')
                fi
        fi
        printf "%8d  %s\n" "$conns" "$cmd"
done
```

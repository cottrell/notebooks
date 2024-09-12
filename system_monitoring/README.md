# 2024-09-09

More OOM.

Found PID via

    grep -5 -i "killed process" /var/log/syslog

(or perhaps other means). Then

    atop -r

    <I> <PID> to search for PID
    <t> <T> forward back until you find it in history
    <c> to show command line view and hopefully you see something more informative than just "python" or whatever. I think the first entry is the full command.


No way to track PID to process (other than python).

Try to enable this for next time:

    sudo apt install auditd
    sudo auditctl -a exit,always -F arch=b64 -S execve

Then (maybe) something like

    ausearch -k python_exec


# 2024-09-06

    sudo apt-get install atop
    sudo systemctl enable atop
    sudo systemctl start atop
    sudo atop -r /var/log/atop/atop_20240905

    sudo apt-get install acct
    sudo systemctl start acct
    sudo systemctl enable acct
    lastcomm

    # for debugging specific things (not running constantly)
    pip install psrecord
    psrecord 1234 --interval 0.1 --log activity.log

    atop-gpu ???


# 2024


Reminders (for post mortem)

    sudo dmesg -T ... this might get you a PID before the OOM

    sar -r   # Shows memory usage over time
    sar -u   # Shows CPU usage over time
    sar -S   # Shows swap usage over time


* https://tomscii.sig7.se/2022/07/uMon-stupid-simple-monitoring
* glances
* systar (sar):

    sudo apt install sysstat  # On Ubuntu/Debian
    sudo systemctl enable --now sysstat

    sar -r 10 100   # Logs memory usage every 10 seconds for 100 intervals

    # post event debug
    sar -u -f /var/log/sysstat/sa05 # cpu
    sar -r -f /var/log/sysstat/sa05 # memory
    sar -q -f /var/log/sysstat/sa05 # load
    sar -b -f /var/log/sysstat/sa05 # i/o

    sudo apt install acct  # then can use lastcomm

* dstat (htop for sar)
* collectl
* netdata


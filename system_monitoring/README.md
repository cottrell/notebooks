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

* https://tomscii.sig7.se/2022/07/uMon-stupid-simple-monitoring
* glances
* systar (sar):

    sudo apt install sysstat  # On Ubuntu/Debian
    sudo systemctl enable --now sysstat

    sar -r   # Shows memory usage over time
    sar -u   # Shows CPU usage over time
    sar -S   # Shows swap usage over time

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


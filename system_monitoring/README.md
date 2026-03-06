# 2026-02-06

## OOM Event Analysis - Chrome Virtual Memory Issue

**Event**: OOM kill at 14:02:46, killed Chrome process (pid 1298503)

**Root Cause**: Chrome renderer processes allocating excessive virtual memory (~1.4TB VSZ each)
- Found 30+ Chrome processes with VSZ > 1TB
- Actual RSS much smaller (300-600MB per process)
- Chrome version: 144.0.7559.59
- oom_score_adj=300 makes these prime targets for OOM killer

**Also Found**:
- NVIDIA GPU out-of-memory errors (Feb 2-5)
- GPU using 1728MB/8192MB (21%)
- Previous OOM kill: Feb 6 03:12:39 (Chrome pid 459803, 3.5GB RSS)

**Monitoring Setup**:
- Created `memory_monitor.py` - tracks RAM, Chrome VSZ, GPU memory
- Logs to `~/.local/log/memory_monitor.log`
- Thresholds: RAM warning 85%, critical 95%, Chrome VSZ > 1TB
- atop running: `/var/log/atop/atop_20260206`

**To investigate with atop**:
```bash
sudo atop -r /var/log/atop/atop_20260206
# <t> to go forward in time to ~14:02
# <c> to show command view
# <m> to sort by memory
```

**Next Steps**:
1. Try Chrome with `--disable-gpu` flag to see if GPU issues related
2. Check for problematic extensions
3. Consider adding systemd service for memory_monitor.py
4. Investigate if Chrome/Wayland interaction causing VSZ bloat

---

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


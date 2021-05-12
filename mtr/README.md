Be aware that potentially high packet loss on one hop and not subsequent might be ok? https://www.datapacket.com/blog/mtr-diagnose-network-issues

Basically a single high packet loss is ok but a monotonic increasing packet loss indicates problems.

https://www.linkedin.com/pulse/diagnosing-network-issues-mtr-priyanka-kumari/

See https://serverfault.com/questions/97277/high-percentage-of-lost-packets-tcp-icmp-mtr-complain-to-isp

mtr --report www.google.com

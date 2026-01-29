# 2024-09-10

    dd if=/dev/zero of=testfile bs=1M count=100 conv=fdatasync

    dd if=testfile of=/dev/null bs=1M count=100 iflag=direct

See also

    sudo apt install fio

    fio --name=write_test --filename=testfile --size=1G --bs=1M --rw=write --direct=1 --numjobs=1 --time_based --runtime=60 --group_reporting

    fio --name=read_test --filename=testfile --size=1G --bs=4K --rw=randread --direct=1 --numjobs=1 --time_based --runtime=60 --group_reporting

    sudo hdparm -tT /dev/sdc

    gnome-disks


## sandisk

    $ sudo fio --name=write_test --filename=testfile --size=1G --bs=1M --rw=write --direct=1 --numjobs=1 --time_based --runtime=60 --group_reporting
    write_test: (g=0): rw=write, bs=(R) 1024KiB-1024KiB, (W) 1024KiB-1024KiB, (T) 1024KiB-1024KiB, ioengine=psync, iodepth=1
    fio-3.36
    Starting 1 process
    write_test: Laying out IO file (1 file / 1024MiB)
    Jobs: 1 (f=1): [W(1)][100.0%][w=5125KiB/s][w=5 IOPS][eta 00m:00s]
    write_test: (groupid=0, jobs=1): err= 0: pid=3625845: Tue Sep 10 10:13:42 2024
      write: IOPS=4, BW=4490KiB/s (4597kB/s)(264MiB/60212msec); 0 zone resets
        clat (msec): min=41, max=1716, avg=228.00, stdev=176.98
         lat (msec): min=41, max=1716, avg=228.06, stdev=176.98
        clat percentiles (msec):
         |  1.00th=[   43],  5.00th=[   45], 10.00th=[   45], 20.00th=[   84],
         | 30.00th=[  100], 40.00th=[  232], 50.00th=[  236], 60.00th=[  279],
         | 70.00th=[  292], 80.00th=[  326], 90.00th=[  330], 95.00th=[  338],
         | 99.00th=[  818], 99.50th=[ 1636], 99.90th=[ 1720], 99.95th=[ 1720],
         | 99.99th=[ 1720]
       bw (  KiB/s): min= 2048, max=22528, per=100.00%, avg=4724.77, stdev=2897.94, samples=114
       iops        : min=    2, max=   22, avg= 4.61, stdev= 2.83, samples=114
      lat (msec)   : 50=14.39%, 100=16.67%, 250=21.21%, 500=45.83%, 1000=1.14%
      lat (msec)   : 2000=0.76%
      cpu          : usr=0.02%, sys=0.20%, ctx=2317, majf=0, minf=10
      IO depths    : 1=100.0%, 2=0.0%, 4=0.0%, 8=0.0%, 16=0.0%, 32=0.0%, >=64=0.0%
         submit    : 0=0.0%, 4=100.0%, 8=0.0%, 16=0.0%, 32=0.0%, 64=0.0%, >=64=0.0%
         complete  : 0=0.0%, 4=100.0%, 8=0.0%, 16=0.0%, 32=0.0%, 64=0.0%, >=64=0.0%
         issued rwts: total=0,264,0,0 short=0,0,0,0 dropped=0,0,0,0
         latency   : target=0, window=0, percentile=100.00%, depth=1

    Run status group 0 (all jobs):
      WRITE: bw=4490KiB/s (4597kB/s), 4490KiB/s-4490KiB/s (4597kB/s-4597kB/s), io=264MiB (277MB), run=60212-60212msec

    Disk stats (read/write):
      sdc: ios=648/2399, sectors=34144/540624, merge=2/44, ticks=12801/102154, in_queue=114956, util=99.95%


    $ sudo     fio --name=read_test --filename=testfile --size=1G --bs=4K --rw=randread --direct=1 --numjobs=1 --time_based --runtime=60 --group_reporting
    read_test: (g=0): rw=randread, bs=(R) 4096B-4096B, (W) 4096B-4096B, (T) 4096B-4096B, ioengine=psync, iodepth=1
    fio-3.36
    Starting 1 process
    Jobs: 1 (f=1): [r(1)][100.0%][r=13.8MiB/s][r=3545 IOPS][eta 00m:00s]
    read_test: (groupid=0, jobs=1): err= 0: pid=3628729: Tue Sep 10 10:15:15 2024
      read: IOPS=3793, BW=14.8MiB/s (15.5MB/s)(889MiB/60001msec)
        clat (nsec): min=1254, max=12884k, avg=262115.28, stdev=443965.99
         lat (nsec): min=1277, max=12884k, avg=262238.34, stdev=443971.58
        clat percentiles (nsec):
         |  1.00th=[   1272],  5.00th=[   1288], 10.00th=[   1304],
         | 20.00th=[   1416], 30.00th=[   1992], 40.00th=[   3056],
         | 50.00th=[   5344], 60.00th=[   6880], 70.00th=[  14400],
         | 80.00th=[ 954368], 90.00th=[1028096], 95.00th=[1105920],
         | 99.00th=[1236992], 99.50th=[1269760], 99.90th=[1318912],
         | 99.95th=[1335296], 99.99th=[1712128]
       bw (  KiB/s): min=12912, max=17128, per=100.00%, avg=15196.33, stdev=995.80, samples=119
       iops        : min= 3228, max= 4282, avg=3799.08, stdev=248.95, samples=119
      lat (usec)   : 2=30.29%, 4=15.21%, 10=22.42%, 20=6.03%, 50=0.20%
      lat (usec)   : 100=0.01%, 250=0.01%, 500=0.01%, 750=2.41%, 1000=9.78%
      lat (msec)   : 2=13.62%, 4=0.01%, 10=0.01%, 20=0.01%
      cpu          : usr=1.25%, sys=3.77%, ctx=58865, majf=0, minf=12
      IO depths    : 1=100.0%, 2=0.0%, 4=0.0%, 8=0.0%, 16=0.0%, 32=0.0%, >=64=0.0%
         submit    : 0=0.0%, 4=100.0%, 8=0.0%, 16=0.0%, 32=0.0%, 64=0.0%, >=64=0.0%
         complete  : 0=0.0%, 4=100.0%, 8=0.0%, 16=0.0%, 32=0.0%, 64=0.0%, >=64=0.0%
         issued rwts: total=227591,0,0,0 short=0,0,0,0 dropped=0,0,0,0
         latency   : target=0, window=0, percentile=100.00%, depth=

    Run status group 0 (all jobs):
       READ: bw=14.8MiB/s (15.5MB/s), 14.8MiB/s-14.8MiB/s (15.5MB/s-15.5MB/s), io=889MiB (932MB), run=60001-60001msec

    Disk stats (read/write):
      sdc: ios=58676/3, sectors=469408/32, merge=0/1, ticks=56511/12, in_queue=56523, util=99.91%


## Generic TR

    $ sudo fio --name=write_test --filename=testfile --size=1G --bs=1M --rw=write --direct=1 --numjobs=1 --time_based --runtime=60 --group_reporting
    write_test: (g=0): rw=write, bs=(R) 1024KiB-1024KiB, (W) 1024KiB-1024KiB, (T) 1024KiB-1024KiB, ioengine=psync, iodepth=1
    fio-3.36
    Starting 1 process
    write_test: Laying out IO file (1 file / 1024MiB)
    Jobs: 1 (f=1): [W(1)][100.0%][w=10.0MiB/s][w=10 IOPS][eta 00m:00s]
    write_test: (groupid=0, jobs=1): err= 0: pid=3667493: Tue Sep 10 10:47:30 2024
      write: IOPS=7, BW=7720KiB/s (7905kB/s)(453MiB/60087msec); 0 zone resets
        clat (msec): min=84, max=2464, avg=132.57, stdev=241.56
         lat (msec): min=84, max=2464, avg=132.63, stdev=241.56
        clat percentiles (msec):
         |  1.00th=[   92],  5.00th=[   93], 10.00th=[   94], 20.00th=[   95],
         | 30.00th=[   95], 40.00th=[   95], 50.00th=[   95], 60.00th=[   96],
         | 70.00th=[   96], 80.00th=[   96], 90.00th=[  116], 95.00th=[  134],
         | 99.00th=[ 1854], 99.50th=[ 2265], 99.90th=[ 2467], 99.95th=[ 2467],
         | 99.99th=[ 2467]
       bw (  KiB/s): min= 2048, max=12288, per=100.00%, avg=9543.26, stdev=2506.30, samples=97
       iops        : min=    2, max=   12, avg= 9.32, stdev= 2.45, samples=97
      lat (msec)   : 100=85.65%, 250=11.26%, 500=1.55%, 2000=0.66%, >=2000=0.88%
      cpu          : usr=0.03%, sys=0.32%, ctx=3698, majf=0, minf=10
      IO depths    : 1=100.0%, 2=0.0%, 4=0.0%, 8=0.0%, 16=0.0%, 32=0.0%, >=64=0.0%
         submit    : 0=0.0%, 4=100.0%, 8=0.0%, 16=0.0%, 32=0.0%, 64=0.0%, >=64=0.0%
         complete  : 0=0.0%, 4=100.0%, 8=0.0%, 16=0.0%, 32=0.0%, 64=0.0%, >=64=0.0%
         issued rwts: total=0,453,0,0 short=0,0,0,0 dropped=0,0,0,0
         latency   : target=0, window=0, percentile=100.00%, depth=1

    Run status group 0 (all jobs):
      WRITE: bw=7720KiB/s (7905kB/s), 7720KiB/s-7720KiB/s (7905kB/s-7905kB/s), io=453MiB (475MB), run=60087-60087msec

    Disk stats (read/write):
      sdc: ios=0/4153, sectors=0/939152, merge=0/47, ticks=0/114133, in_queue=114133, util=98.45%


    $ sudo     fio --name=read_test --filename=testfile --size=1G --bs=4K --rw=randread --direct=1 --numjobs=1 --time_based --runtime=60 --group_reporting
    read_test: (g=0): rw=randread, bs=(R) 4096B-4096B, (W) 4096B-4096B, (T) 4096B-4096B, ioengine=psync, iodepth=1
    fio-3.36
    Starting 1 process
    Jobs: 1 (f=1): [r(1)][100.0%][r=9037KiB/s][r=2259 IOPS][eta 00m:00s]
    read_test: (groupid=0, jobs=1): err= 0: pid=3754144: Tue Sep 10 10:51:22 2024
      read: IOPS=2217, BW=8870KiB/s (9083kB/s)(520MiB/60001msec)
        clat (nsec): min=1250, max=9422.2k, avg=448083.24, stdev=520508.94
         lat (nsec): min=1269, max=9423.0k, avg=448335.43, stdev=520523.69
        clat percentiles (nsec):
         |  1.00th=[   1288],  5.00th=[   1320], 10.00th=[   1704],
         | 20.00th=[   3600], 30.00th=[   6880], 40.00th=[   9024],
         | 50.00th=[  15424], 60.00th=[ 741376], 70.00th=[ 839680],
         | 80.00th=[ 937984], 90.00th=[1236992], 95.00th=[1384448],
         | 99.00th=[1548288], 99.50th=[1597440], 99.90th=[1728512],
         | 99.95th=[1777664], 99.99th=[1875968]
       bw (  KiB/s): min= 7712, max=10704, per=100.00%, avg=8873.48, stdev=659.96, samples=119
       iops        : min= 1928, max= 2676, avg=2218.37, stdev=164.99, samples=119
      lat (usec)   : 2=12.31%, 4=8.26%, 10=21.22%, 20=13.35%, 50=0.35%
      lat (usec)   : 100=0.02%, 250=0.01%, 500=0.01%, 750=5.41%, 1000=23.40%
      lat (msec)   : 2=15.67%, 4=0.01%, 10=0.01%
      cpu          : usr=1.35%, sys=4.68%, ctx=59239, majf=0, minf=14
      IO depths    : 1=100.0%, 2=0.0%, 4=0.0%, 8=0.0%, 16=0.0%, 32=0.0%, >=64=0.0%
         submit    : 0=0.0%, 4=100.0%, 8=0.0%, 16=0.0%, 32=0.0%, 64=0.0%, >=64=0.0%
         complete  : 0=0.0%, 4=100.0%, 8=0.0%, 16=0.0%, 32=0.0%, 64=0.0%, >=64=0.0%
         issued rwts: total=133056,0,0,0 short=0,0,0,0 dropped=0,0,0,0
         latency   : target=0, window=0, percentile=100.00%, depth=1

    Run status group 0 (all jobs):
       READ: bw=8870KiB/s (9083kB/s), 8870KiB/s-8870KiB/s (9083kB/s-9083kB/s), io=520MiB (545MB), run=60001-60001msec

    Disk stats (read/write):
      sdc: ios=59079/3, sectors=472632/32, merge=0/1, ticks=55898/19, in_queue=55917, util=99.95%


## TR

Chipsbank Microelectronics Co., Ltd Flash Disk

    write_test: (g=0): rw=write, bs=(R) 1024KiB-1024KiB, (W) 1024KiB-1024KiB, (T) 1024KiB-1024KiB, ioengine=psync, iodepth=1
    fio-3.36
    Starting 1 process
    write_test: Laying out IO file (1 file / 1024MiB)
    Jobs: 1 (f=1): [W(1)][100.0%][w=5125KiB/s][w=5 IOPS][eta 00m:00s]
    write_test: (groupid=0, jobs=1): err= 0: pid=3760332: Tue Sep 10 11:02:56 2024
      write: IOPS=3, BW=3842KiB/s (3934kB/s)(227MiB/60505msec); 0 zone resets
        clat (msec): min=214, max=1425, avg=266.48, stdev=156.59
         lat (msec): min=215, max=1425, avg=266.53, stdev=156.59
        clat percentiles (msec):
         |  1.00th=[  215],  5.00th=[  215], 10.00th=[  218], 20.00th=[  218],
         | 30.00th=[  218], 40.00th=[  218], 50.00th=[  232], 60.00th=[  232],
         | 70.00th=[  232], 80.00th=[  234], 90.00th=[  300], 95.00th=[  535],
         | 99.00th=[ 1116], 99.50th=[ 1368], 99.90th=[ 1418], 99.95th=[ 1418],
         | 99.99th=[ 1418]
       bw (  KiB/s): min= 2043, max= 6144, per=100.00%, avg=4095.84, stdev=1160.98, samples=113
       iops        : min=    1, max=    6, avg= 3.98, stdev= 1.14, samples=113
      lat (msec)   : 250=88.55%, 500=5.29%, 750=3.96%, 1000=0.88%, 2000=1.32%
      cpu          : usr=0.05%, sys=0.12%, ctx=1951, majf=0, minf=11
      IO depths    : 1=100.0%, 2=0.0%, 4=0.0%, 8=0.0%, 16=0.0%, 32=0.0%, >=64=0.0%
         submit    : 0=0.0%, 4=100.0%, 8=0.0%, 16=0.0%, 32=0.0%, 64=0.0%, >=64=0.0%
         complete  : 0=0.0%, 4=100.0%, 8=0.0%, 16=0.0%, 32=0.0%, 64=0.0%, >=64=0.0%
         issued rwts: total=0,227,0,0 short=0,0,0,0 dropped=0,0,0,0
         latency   : target=0, window=0, percentile=100.00%, depth=1

    Run status group 0 (all jobs):
      WRITE: bw=3842KiB/s (3934kB/s), 3842KiB/s-3842KiB/s (3934kB/s-3934kB/s), io=227MiB (238MB), run=60505-60505msec

    Disk stats (read/write):
      sdd: ios=0/2265, sectors=0/509984, merge=0/53, ticks=0/114870, in_queue=114870, util=100.00%


    sudo fio --name=read_test --filename=testfile --size=1G --bs=4K --rw=randread --direct=1 --numjobs=1 --time_based --runtime=60 --group_reporting
    read_test: (g=0): rw=randread, bs=(R) 4096B-4096B, (W) 4096B-4096B, (T) 4096B-4096B, ioengine=psync, iodepth=1
    fio-3.36
    Starting 1 process
    Jobs: 1 (f=1): [r(1)][100.0%][r=32.2MiB/s][r=8240 IOPS][eta 00m:00s]
    read_test: (groupid=0, jobs=1): err= 0: pid=3761048: Tue Sep 10 11:04:46 2024
      read: IOPS=7288, BW=28.5MiB/s (29.9MB/s)(1708MiB/60001msec)
        clat (nsec): min=1093, max=226324k, avg=136427.12, stdev=823053.92
         lat (nsec): min=1111, max=226324k, avg=136490.31, stdev=823055.80
        clat percentiles (nsec):
         |  1.00th=[    1128],  5.00th=[    1144], 10.00th=[    1144],
         | 20.00th=[    1160], 30.00th=[    1176], 40.00th=[    1208],
         | 50.00th=[    1512], 60.00th=[    2832], 70.00th=[    5984],
         | 80.00th=[  382976], 90.00th=[  651264], 95.00th=[  716800],
         | 99.00th=[  815104], 99.50th=[  864256], 99.90th=[  954368],
         | 99.95th=[  995328], 99.99th=[25559040]
       bw (  KiB/s): min= 2960, max=38976, per=99.93%, avg=29135.87, stdev=6039.41, samples=119
       iops        : min=  740, max= 9744, avg=7283.97, stdev=1509.85, samples=119
      lat (usec)   : 2=56.73%, 4=10.89%, 10=8.54%, 20=1.61%, 50=0.07%
      lat (usec)   : 100=0.01%, 250=0.01%, 500=9.74%, 750=9.61%, 1000=2.76%
      lat (msec)   : 2=0.03%, 4=0.01%, 10=0.01%, 20=0.01%, 50=0.01%
      lat (msec)   : 100=0.01%, 250=0.01%
      cpu          : usr=1.22%, sys=3.48%, ctx=96990, majf=0, minf=13
      IO depths    : 1=100.0%, 2=0.0%, 4=0.0%, 8=0.0%, 16=0.0%, 32=0.0%, >=64=0.0%
         submit    : 0=0.0%, 4=100.0%, 8=0.0%, 16=0.0%, 32=0.0%, 64=0.0%, >=64=0.0%
         complete  : 0=0.0%, 4=100.0%, 8=0.0%, 16=0.0%, 32=0.0%, 64=0.0%, >=64=0.0%
         issued rwts: total=437330,0,0,0 short=0,0,0,0 dropped=0,0,0,0
         latency   : target=0, window=0, percentile=100.00%, depth=1

    Run status group 0 (all jobs):
       READ: bw=28.5MiB/s (29.9MB/s), 28.5MiB/s-28.5MiB/s (29.9MB/s-29.9MB/s), io=1708MiB (1791MB), run=60001-60001msec

    Disk stats (read/write):
      sdd: ios=96711/137, sectors=773688/28800, merge=0/5, ticks=54867/4483, in_queue=59350, util=99.90%


    ### 1. **SanDisk**:
    - **Write Speed**: ~4.5 MB/s
    - **Read Speed**: ~15.5 MB/s

    ### 2. **Generic TR**:
    - **Write Speed**: ~7.5 MB/s
    - **Read Speed**: ~9 MB/s

    ### 3. **Chipsbank Microelectronics (Flash Disk)**:
    - **Write Speed**: ~3.9 MB/s (the slowest write speed)
    - **Read Speed**: ~29.9 MB/s (the best read speed)

    ### Conclusion:
    - **SanDisk**: Moderate write speed and decent read speed.
    - **Generic TR**: Better write speed than SanDisk, but lower read speed.
    - **Chipsbank**: Poor write speed (the worst) but **much better read speed** than the other two drives.

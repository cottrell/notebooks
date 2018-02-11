# https://github.com/docker-library/docs/tree/master/centos#systemd-integration
# see ../docker/c7-systemd

FROM local/c7-systemd
# need this for centos7 or user mariadb
RUN rpm -Uvh http://dev.mysql.com/get/mysql-community-release-el7-5.noarch.rpm; yum -y install mysql-server; systemctl enable mysqld.service
CMD ["/usr/sbin/init"]
# ls /var/lib/mysql/ib_logfile* > /dev/null 2>&1 && mkdir -p /var/lib/mysql/ib_logfile.bak  && mv /var/lib/mysql/ib_logfile* /var/lib/mysql/ib_logfile.bak

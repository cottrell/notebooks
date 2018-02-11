# https://github.com/docker-library/docs/tree/master/centos#systemd-integration
# https://github.com/CentOS/CentOS-Dockerfiles/tree/master/mariadb/centos7
# see ../docker/c7-systemd
FROM local/c7-systemd
RUN yum -y install mariadb-server mariadb; yum clean all; systemctl enable mariadb.service
CMD ["/usr/sbin/init"]
EXPOSE 3306

# https://www.cloudera.com/documentation/enterprise/latest/topics/install_cm_mariadb.html#install_cm_mariadb_config
# TODO: It is important that the datadir directory, which, by default, is /var/lib/mysql, is on a partition that has sufficient free space.
RUN systemctl check mariadb.service
RUN systemctl stop mariadb.service
# RUN ls /var/lib/mysql/ib_logfile* > /dev/null 2>&1 && mkdir -p /var/lib/mysql/ib_logfile.bak  && mv /var/lib/mysql/ib_logfile* /var/lib/mysql/ib_logfile.bak
# COPY base_my.cnf cloudera_recommended_my.cnf /tmp
# # TODO: update /etc/my.cnf
# # If AppArmor is running on the host where MariaDB is installed, you might need to configure AppArmor to allow MariaDB to write to the binary.
# RUN systemctl start mariadb.service
# # Set the MariaDB root password. In the following example, the current root password is blank. Press the Enter key when you're prompted for the root password.
# # RUN /usr/bin/mysql_secure_installation # this is interactive?
# 
# # Installing the MySQL JDBC Driver for MariaDB
# # Important: Do not use the yum install command to install the MySQL driver package, because it installs openJDK, and then uses the Linux alternatives command to set the system JDK to be openJDK.
# # http://www.mysql.com/downloads/connector/j/5.1.html ... might need to sign in?
# # Copy the JDBC driver, renamed, to the relevant host.
# RUN wget https://dev.mysql.com/get/Downloads/Connector-J/mysql-connector-java-5.1.45.tar.gz; \
#     tar xvzf tar zxvf mysql-connector-java-5.1.45.tar.gz; \
#     mkdir -p /usr/share/java; \
#     cp mysql-connector-java-5.1.45/mysql-connector-java-5.1.45-bin.jar /usr/share/java/mysql-connector-java.jar


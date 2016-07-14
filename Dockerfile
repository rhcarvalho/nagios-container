FROM centos:centos7

EXPOSE 8080

ADD sendEmail-epel-7.repo /etc/yum.repos.d/

RUN yum install -y epel-release && \
    INSTALL_PKGS="httpd nagios telnet supervisor python-jinja2 nagios-plugins-all sendEmail perl-Net-SSLeay perl-IO-Socket-SSL jq" && \
    yum -y --setopt=tsflags=nodocs install $INSTALL_PKGS && \
    rpm -V $INSTALL_PKGS && \
    yum clean all && \
    curl --retry 999 --retry-max-time 0 -sSL https://github.com/openshift/origin/releases/download/v1.2.0/openshift-origin-client-tools-v1.2.0-2e62fab-linux-64bit.tar.gz | tar xzv && \
    mv openshift-origin-*/* /usr/bin/ \
    mkdir -p /opt/rhmap/ && \
    sed -i -e 's/Listen 80/Listen 8080/' \
           -e 's|DocumentRoot "/var/www/html"|DocumentRoot "/usr/share/nagios/html"|' \
           -e 's|<Directory "/var/www">|<Directory "/usr/share/nagios/html">|' \
           /etc/httpd/conf/httpd.conf && \
    touch /supervisord.log /supervisord.pid && \
    mkdir -p /var/log/nagios/archives /var/log/nagios/rw/ /var/log/nagios/spool/checkresults /opt/rhmap/nagios/plugins/ && \
    chmod -R 777 /supervisord.log /supervisord.pid /var/log/nagios \
                 /etc/httpd /etc/passwd /var/log /etc/nagios /usr/lib64/nagios \
                 /var/spool/nagios /run /usr/share/httpd /usr/share/nagios && \
    sed -i -e 's|cfg_file=/etc/nagios/objects/localhost.cfg||' /etc/nagios/nagios.cfg

ADD supervisord.conf /etc/supervisord.conf
ADD make-nagios-fhservices-cfg make-nagios-commands-cfg fhservices.cfg.j2 commands.cfg.j2 /opt/rhmap/
ADD plugins/default/* plugins/core/* /opt/rhmap/nagios/plugins/
RUN chmod -R 755 /opt/rhmap/nagios/plugins/
ADD start /start

CMD ["/start"]
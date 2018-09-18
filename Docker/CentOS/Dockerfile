
# "ported" by Adam Miller <maxamillion@fedoraproject.org> from
#   https://github.com/fedora-cloud/Fedora-Dockerfiles
#
# Originally written for Fedora-Dockerfiles by
#   scollier <scollier@redhat.com>

FROM centos:centos7
MAINTAINER The CentOS Project <cloud-ops@centos.org>

RUN yum -y update; yum clean all
RUN yum -y install openssh-server passwd; yum clean all
ADD ./start.sh /start.sh
RUN mkdir /var/run/sshd
RUN echo 'root:root' | chpasswd

RUN ssh-keygen -t rsa -f /etc/ssh/ssh_host_rsa_key -N '' 

# EXPOSE 22
ENTRYPOINT ["/usr/sbin/sshd", "-D"]

# Based on:
# https://docs.docker.com/engine/examples/running_ssh_service/

FROM debian:jessie

MAINTAINER Theodotos Andreou <theo@ubuntucy.org>

RUN apt-get update \
    && apt-get -q -y dist-upgrade \
    && apt-get -q -y install --no-install-recommends openssh-server \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN mkdir /var/run/sshd

# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]
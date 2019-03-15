FROM centos:latest

COPY pkg/SaltStack-Sources.repo  /etc/yum.repos.d

RUN yum -y install epel-release
RUN yum -y update
RUN yum -y install openssh-server passwd iproute salt-minion

####### sshd 远程调试使用#######################

RUN mkdir /var/run/sshd
RUN echo 'root:sshpass' | chpasswd
RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd
ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile
RUN ssh-keygen -t rsa -f /etc/ssh/ssh_host_rsa_key -N ''
EXPOSE 22
################################################

COPY test/minion /etc/salt/

COPY test/entrypoint  /opt/run/code/entrypoint
RUN chmod +x /opt/run/code/entrypoint

WORKDIR /opt/run/code
ENTRYPOINT ["/opt/run/code/entrypoint"]


FROM centos:latest

RUN yum -y install epel-release
RUN yum -y update
RUN yum -y install openssh-server passwd gcc gcc-c++ make libpq-dev git sshpass libffi-devel zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel

ADD pkg/Python-3.7.2.tgz /opt/run/code
RUN cd /opt/run/code/Python-3.7.2/ && ./configure && make && make altinstall

COPY pkg/get-pip.py /opt/run/code/get-pip.py
RUN cd /opt/run/code/ && python3.7 get-pip.py
COPY src/requirements.txt /opt/run/code/requirements.txt
RUN cd /opt/run/code/ && pip install -r requirements.txt -i http://pypi.douban.com/simple --trusted-host pypi.douban.com

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

COPY src/entrypoint  /opt/run/code/entrypoint
RUN chmod +x /opt/run/code/entrypoint

WORKDIR /opt/run/code
ENTRYPOINT ["/opt/run/code/entrypoint"]


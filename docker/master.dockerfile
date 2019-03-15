FROM centos:latest

RUN yum -y install epel-release
RUN yum -y update
RUN yum -y install openssh-server passwd

COPY pkg/salt-py3-repo-latest-2.el7.noarch.rpm /opt/run/code/
RUN cd /opt/run/code/ && yum -y install salt-py3-repo-latest-2.el7.noarch.rpm
RUN yum -y update
RUN yum -y install salt-master salt-api salt-ssh

RUN yum -y install python34-pip
RUN pip3 install redis ws4py -i http://pypi.douban.com/simple --trusted-host pypi.douban.com

#COPY pkg/get-pip.py /opt/run/code/get-pip.py
#RUN cd /opt/run/code/ && python3 get-pip.py
#COPY pkg/requirements_master.txt /opt/run/code/requirements.txt
#RUN cd /opt/run/code/ && pip3 install -r requirements.txt -i http://pypi.douban.com/simple --trusted-host pypi.douban.com

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

COPY docker/master /etc/salt/
COPY docker/rest_cherrypy.conf /etc/salt/master.d/
COPY docker/pillar.conf /etc/salt/master.d/
RUN useradd flamingos
RUN echo "flamingos" | passwd flamingos --stdin

COPY pkg/redismod.py /usr/lib/python3.4/site-packages/salt/modules/redismod.py
COPY src/event_sender.py /opt/run/code/event_sender.py

COPY docker/entrypoint_master  /opt/run/code/entrypoint
RUN chmod +x /opt/run/code/entrypoint

WORKDIR /opt/run/code
ENTRYPOINT ["/opt/run/code/entrypoint"]
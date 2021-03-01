FROM centos:7
RUN yum install epel* -y;yum install python-pip nfs-utils -y;pip install --upgrade --force-reinstall pip==9.0.3;pip install kubernetes
RUN yum install gcc python-devel* -y;pip install ipconflict netaddr paramiko jinja2
VOLUME ["/home/install_sly", '/root/.kube']


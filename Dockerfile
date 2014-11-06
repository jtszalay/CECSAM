FROM ubuntu:12.04
RUN apt-get update

# runit stuffs
RUN apt-get install -y runit
ADD runit/init-i /sbin/init-i
RUN chmod +x /sbin/init-i
ENTRYPOINT ["/sbin/init-i"]
ONBUILD ENTRYPOINT ["/sbin/init-i"]

# app stuffs
RUN apt-get install -y python-virtualenv python-dev git-core 
RUN mkdir /opt/CECSAM
ADD . /opt/CECSAM/
ADD runit/service /service

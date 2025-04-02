FROM ubuntu:22.04

# Environment variables for Hadoop and Java
ENV HADOOP_VERSION=3.3.6
ENV HADOOP_HOME=/opt/hadoop
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

# Install required packages
RUN apt-get update && apt-get install -y \
    openjdk-11-jdk wget curl openssh-client openssh-server vim && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Download and install Hadoop
RUN wget -q https://downloads.apache.org/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz && \
    tar -xvzf hadoop-${HADOOP_VERSION}.tar.gz && \
    mv hadoop-${HADOOP_VERSION} ${HADOOP_HOME} && \
    rm hadoop-${HADOOP_VERSION}.tar.gz

# Configure SSH
RUN mkdir -p /var/run/sshd && \
    ssh-keygen -t rsa -N '' -f /root/.ssh/id_rsa && \
    cat /root/.ssh/id_rsa.pub >> /root/.ssh/authorized_keys && \
    chmod 600 /root/.ssh/authorized_keys && \
    chmod 700 /root/.ssh

RUN echo "export JAVA_HOME=${JAVA_HOME}" >> ${HADOOP_HOME}/etc/hadoop/hadoop-env.sh

RUN useradd -m -d /home/hadoop -s /bin/bash hadoop && \
    chown -R hadoop:hadoop ${HADOOP_HOME}

WORKDIR /home/hadoop

COPY sensor_measurements_data.txt /data/
COPY mapper.py reducer.py /scripts/
RUN chown -R hadoop:hadoop /data /scripts && chmod +x /scripts/mapper.py /scripts/reducer.py

USER hadoop

CMD ["/bin/bash"]

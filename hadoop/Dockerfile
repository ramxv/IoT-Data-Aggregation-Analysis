FROM ubuntu:22.04

WORKDIR ${HADOOP_HOME}

# Set environment variables
ENV HADOOP_VERSION=3.3.6
ENV HADOOP_HOME=/opt/hadoop
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

# Install necessary packages
RUN apt-get update && apt-get install -y \
    openjdk-11-jdk wget ssh vim curl python3 python3-pip \
    && apt-get clean

# Download and install Hadoop
RUN wget https://downloads.apache.org/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz && \
    tar -xvzf hadoop-${HADOOP_VERSION}.tar.gz && \
    mv hadoop-${HADOOP_VERSION} ${HADOOP_HOME} && \
    rm hadoop-${HADOOP_VERSION}.tar.gz

# Configure SSH (needed for Hadoop in pseudo-distributed mode)
RUN apt-get install -y openssh-server && \
    ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa && \
    cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys && \
    chmod 600 ~/.ssh/authorized_keys

RUN ${HADOOP_HOME}/bin/hdfs namenode -format

# Set Hadoop environment variables
RUN echo "export JAVA_HOME=${JAVA_HOME}" >> ${HADOOP_HOME}/etc/hadoop/hadoop-env.sh

COPY sensor_measurements_data.txt .

COPY mapper.py /scripts/
COPY reducer.py /scripts/

# Set execution permissions
RUN chmod +x /scripts/mapper.py /scripts/reducer.py

CMD ["/bin/bash"]

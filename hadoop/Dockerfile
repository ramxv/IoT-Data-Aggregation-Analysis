FROM ubuntu:22.04

ENV HADOOP_VERSION=3.3.6
ENV HADOOP_HOME=/opt/hadoop
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

# Install necessary packages
RUN apt-get update && apt-get install -y \
    openjdk-11-jdk wget curl openssh-client \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Download and install Hadoop
RUN wget https://downloads.apache.org/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz && \
    tar -xvzf hadoop-${HADOOP_VERSION}.tar.gz && \
    mv hadoop-${HADOOP_VERSION} ${HADOOP_HOME} && \
    rm hadoop-${HADOOP_VERSION}.tar.gz || { echo "Download failed"; exit 1; }

# Set Hadoop environment variables
RUN echo "export JAVA_HOME=${JAVA_HOME}" >> ${HADOOP_HOME}/etc/hadoop/hadoop-env.sh

COPY sensor_measurements_data.txt /data/
COPY mapper.py /scripts/
COPY reducer.py /scripts/

RUN chmod +x /scripts/mapper.py /scripts/reducer.py

# Create and switch to non-root user
RUN useradd -m hadoop && \
    chown -R hadoop:hadoop ${HADOOP_HOME} /data /scripts

USER hadoop

WORKDIR ${HADOOP_HOME}

# Set Hadoop configuration (optional - if you have custom configs)
#COPY core-site.xml ${HADOOP_HOME}/etc/hadoop/
#COPY hdfs-site.xml ${HADOOP_HOME}/etc/hadoop/

CMD ["/bin/bash"]

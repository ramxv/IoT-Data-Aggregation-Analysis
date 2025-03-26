FROM ubuntu:22.04

# Environment variables for Hadoop and Java
ENV HADOOP_VERSION=3.3.6
ENV HADOOP_HOME=/opt/hadoop
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

# Install required packages
RUN apt-get update && apt-get install -y \
    openjdk-11-jdk wget curl openssh-client && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Download and install Hadoop
RUN wget https://downloads.apache.org/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz && \
    tar -xvzf hadoop-${HADOOP_VERSION}.tar.gz && \
    mv hadoop-${HADOOP_VERSION} ${HADOOP_HOME} && \
    rm hadoop-${HADOOP_VERSION}.tar.gz || { echo "Download failed"; exit 1; }

# Configure Hadoop to use the correct Java home
RUN echo "export JAVA_HOME=${JAVA_HOME}" >> ${HADOOP_HOME}/etc/hadoop/hadoop-env.sh

# Copy the sensor data file and the MapReduce scripts
COPY sensor_measurements_data.txt /data/
COPY mapper.py reducer.py /scripts/
RUN chmod +x /scripts/mapper.py /scripts/reducer.py

# Create a non-root user and assign proper permissions
RUN useradd -m hadoop && \
    chown -R hadoop:hadoop ${HADOOP_HOME} /data /scripts

# Switch to non-root user and set working directory
USER hadoop
WORKDIR ${HADOOP_HOME}

# Start a bash shell (manual commands can now be executed)
CMD ["/bin/bash"]
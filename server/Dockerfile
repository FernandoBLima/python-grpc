# Base image
FROM python:3.9

# Metainfo
LABEL org.label-schema.name="grpc-python-server" \
      org.label-schema.description="A python project that contains grpc server" \
      org.label-schema.build-date="${build_date}" \
      org.label-schema.schema-version="1.0" \
      maintainer="Fernando Lima"

# Adding HOME and setting as workdir
ENV HOME /home/app
WORKDIR $HOME
USER root

# Make a directory for app
WORKDIR /server

COPY setup.py .
COPY requirements.txt .

# # Install Python base packages
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --upgrade setuptools certifi
RUN pip install --no-cache-dir -r requirements.txt

# Copy protobufer
COPY ./protos .

# Copy application
COPY . .

# Generate proto files
RUN python3.9 -m grpc_tools.protoc -I ./protos --python_out=. --grpc_python_out=. ./protos/model.proto

# Add non root user
RUN adduser app
USER app

# Default command
CMD ["python3.9", "app.py"]
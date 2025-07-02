FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Install base tools and Python environment
RUN apt-get update -y && apt-get upgrade -y && \
    apt-get install -y \
    bash curl git jq build-essential \
    python3 python3-pip python3-venv python3-dev

WORKDIR /vagrant

CMD ["bash"]

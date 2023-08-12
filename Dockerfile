ARG BASE_IMAGE=python:3.9-slim
FROM $BASE_IMAGE as runtime-environment


COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh
# install project requirements
COPY src/requirements.txt /tmp/requirements.txt
RUN apt-get update && apt-get install -y build-essential
RUN pip3 install --no-cache -r /tmp/requirements.txt && rm -f /tmp/requirements.txt

# add kedro user
ARG KEDRO_UID=999
ARG KEDRO_GID=0
RUN groupadd -f -g ${KEDRO_GID} kedro_group && \
useradd -m -d /home/kedro_docker -s /bin/bash -g ${KEDRO_GID} -u ${KEDRO_UID} kedro_docker

WORKDIR /home/kedro_docker
USER kedro_docker

FROM runtime-environment

# copy the whole project except what is in .dockerignore
ARG KEDRO_UID=999
ARG KEDRO_GID=0
COPY --chown=${KEDRO_UID}:${KEDRO_GID} . .

EXPOSE 8888
EXPOSE 8000
EXPOSE 4141


# Set the entrypoint as the script
ENTRYPOINT ["/entrypoint.sh"]
FROM python:3.13-slim

RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

RUN . /etc/os-release && \
    install -d /usr/share/postgresql-common/pgdg \
    && curl -o /usr/share/postgresql-common/pgdg/apt.postgresql.org.asc \
       https://www.postgresql.org/media/keys/ACCC4CF8.asc \
    && echo "deb [signed-by=/usr/share/postgresql-common/pgdg/apt.postgresql.org.asc] http://apt.postgresql.org/pub/repos/apt ${VERSION_CODENAME}-pgdg main" \
       > /etc/apt/sources.list.d/pgdg.list

RUN apt-get update \
    && apt-get install -y postgresql-client-18 \
    && rm -rf /var/lib/apt/lists/*

COPY elt_script.py .

CMD ["python", "elt_script.py"]
FROM python:3.12-slim-bookworm

ARG dev=false
ENV PIPENV_DEV=${dev}

RUN apt-get update && apt-get -y upgrade \
    && apt-get -y install gcc python3-dev libffi-dev make \
    && pip install --no-cache-dir --upgrade pip pipenv

WORKDIR /root
COPY ./Pipfile ./Pipfile.lock ./
RUN pipenv install --system --ignore-pipfile --deploy

ARG UID=1000

ENV USER=pin
ENV HOME=/srv/app
ENV DJANGO_SETTINGS_MODULE=django_project.settings

RUN addgroup "$USER" \
    && adduser \
    --disabled-password \
    --gecos "" \
    --home "$HOME" \
    --ingroup "$USER" \
    --uid "$UID" \
    "$USER"

USER $USER
WORKDIR $HOME

COPY --chown=$USER:$USER ./ $HOME/

EXPOSE 8000
CMD ["ddtrace-run", "gunicorn"]

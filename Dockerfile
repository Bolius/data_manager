FROM python:3.8

WORKDIR /app

RUN apt-get update && \
    apt-get install -y apt-utils binutils libproj-dev gdal-bin graphviz

RUN wget -O \
        /tmp/sass.tar.gz  \
        https://github.com/sass/dart-sass/releases/download/1.26.7/dart-sass-1.26.7-linux-x64.tar.gz \
    && tar xf /tmp/sass.tar.gz -C /bin \
    && chmod -R a+rx /bin/dart-sass/


COPY pyproject.toml  pyproject.toml
# COPY poetry.lock poetry.lock

ENV POETRY_VIRTUALENVS_CREATE false

RUN pip install --upgrade pip \
    && pip install poetry \
    && poetry install

EXPOSE 8000

ARG arg_debug_mode=False
ENV DEBUG=$arg_debug_mode

COPY entrypoint.sh app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]


COPY . /app


CMD ["gunicorn", "data_store.wsgi:application", \
     "--bind", "0.0.0.0:8000", \
     "--workers" , "4",  \
     "--worker-tmp-dir", "/dev/shm", \
     "--threads", "4", \
     "--worker-class" ,"gthread"]

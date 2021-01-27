FROM python:3.7.2-alpine3.9

RUN pip install --upgrade pip

COPY ./DeterminedApp/requirements.txt .
RUN pip install -r requirements.txt

COPY ./DeterminedApp /app

WORKDIR /app

COPY ./entrypoint.sh /
ENTRYPOINT [ "sh", "/entrypoint.sh" ]
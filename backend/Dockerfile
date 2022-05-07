# pull official base image
FROM python:3.9

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV APP_HOME=/home/backend
RUN mkdir -p $APP_HOME
RUN mkdir $APP_HOME/staticfiles
RUN mkdir $APP_HOME/mediafiles
RUN mkdir $APP_HOME/logs
RUN addgroup --system app && adduser --system --group app
WORKDIR $APP_HOME

COPY ./requirements.txt $APP_HOME/requirements.txt
COPY . $APP_HOME

# install psycopg2 dependencies
RUN apt-get update \
    && apt-get install -y postgresql-server-dev-all gcc python3-dev musl-dev

# update pip
RUN python3 -m pip install --upgrade pip

# install dependencies
RUN python3 -m pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g'  $APP_HOME/entrypoint.sh
RUN chmod +x  $APP_HOME/entrypoint.sh

# chown all the files to the app user
RUN chown -R app:app $APP_HOME
RUN chmod -R 755 $APP_HOME/staticfiles
RUN chmod -R 755 $APP_HOME/mediafiles
RUN chmod -R 755 $APP_HOME/logs

# change to the app user
USER app

# run entrypoint.sh
# ENTRYPOINT ["/home/backend/entrypoint.sh"]
FROM python:3.10

RUN mkdir /test_task_for_webtronics

WORKDIR /test_task_for_webtronics

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x docker/*.sh

#WORKDIR src
#
#CMD uvicorn main:app --host 0.0.0.0 --reload

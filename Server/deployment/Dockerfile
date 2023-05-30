FROM python:3.12.0a7-bullseye
ARG SECRET_KEY
ENV SECRET_KEY ${SECRET_KEY}
WORKDIR /Server/
COPY . /Server/
RUN pip install -r deployment/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --extra-index-url https://mirrors.aliyun.com/pypi/simple/
RUN python manage.py makemigrations
RUN python manage.py collectstatic --noinput
EXPOSE 8000
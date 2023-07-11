FROM python:3.10-slim
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code

COPY apt_requirements.txt /code/
RUN apt-get update && cat apt_requirements.txt | xargs apt -y --no-install-recommends install \
	&& rm -rf /var/lib/apt/lists/* \
	&& apt autoremove \
	&& apt autoclean

ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal


COPY requirements.txt /code/

COPY entrypoint.sh /code/
RUN chmod -R 777 /code/

RUN pip install --no-cache-dir -r requirements.txt


ENTRYPOINT ["sh", "/code/entrypoint.sh"]
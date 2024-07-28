FROM python:3.12
WORKDIR /app
COPY requirements.txt requirements.txt
RUN python3 -m pip install --requirement requirements.txt
COPY . .
RUN cd /app
# CMD /app/scripts/develop
CMD /bin/bash
EXPOSE 8123

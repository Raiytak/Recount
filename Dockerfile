FROM python:3.8
WORKDIR /code
# ENV FLASK_APP=app.py
# ENV FLASK_RUN_HOST=0.0.0.0
# RUN apk add --no-cache gcc musl-dev linux-headers
COPY libraries.txt libraries.txt
RUN pip install -r libraries.txt
EXPOSE 8050
COPY . .
CMD ["app", "run"]
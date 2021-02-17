FROM python:3.8

COPY . .

RUN pip install -r libraries.txt

CMD ["python", "/code/main.py"]
# RUN apk add --no-cache gcc musl-dev linux-headers




# # # Version test flask
# FROM python:3.8
# ENV FLASK_APP=/code/wrapper_excel/app.py
# ENV FLASK_RUN_HOST=0.0.0.0
# # RUN apk add --no-cache gcc musl-dev linux-headers
# COPY requirements.txt requirements.txt
# RUN pip install -r requirements.txt
# EXPOSE 5000
# COPY . .
# CMD /bin/bash -c "flask run"
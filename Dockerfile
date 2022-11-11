FROM python:3.10.8
ADD main.py /

RUN pip install --upgrade pip
RUN pip install primePy
RUN pip install fastapi
RUN pip install Pillow
RUN pip install passlib[bcrypt]
RUN pip install python-multipart
RUN pip install uvicorn

COPY . .

CMD ["python", "main.py"]
EXPOSE 5000
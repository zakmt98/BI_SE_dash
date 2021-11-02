FROM alpine:latest
WORKDIR /BI_project
ADD . /BI_project

RUN pip install -r requirements.txt    
ENTRYPOINT [ "python" ]
CMD [ "main.py" ]

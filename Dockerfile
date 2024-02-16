
FROM public.ecr.aws/docker/library/python:3.11

COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.8.1 /lambda-adapter /opt/extensions/lambda-adapter
WORKDIR /var/task

COPY app/requirements.txt ./
RUN python -m pip install -r requirements.txt

COPY app/app.py ./

ENV MPLCONFIGDIR=/tmp/matplotlib

ENTRYPOINT ["python3"]
CMD ["app.py"]

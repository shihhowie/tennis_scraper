FROM amazon/aws-lambda-python:3.9

RUN yum install -y unzip

COPY ./chrome-installer.sh ./chrome-installer.sh
RUN chmod +x ./chrome-installer.sh
RUN ./chrome-installer.sh
RUN pip install -r requirements.txt

COPY scraper.py ./
CMD ["scraper.lambda_handler"]
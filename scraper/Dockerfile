 FROM amazon/aws-lambda-python:3.9

RUN chmod +x ./chrome-installer.sh
RUN ./chrome-installer.sh
RUN pip install -r requirements.txt

CMD ["scraper.lambda_handler"]
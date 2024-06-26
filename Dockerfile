FROM python:3.10-slim

WORKDIR /evo_bio_computing

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

CMD ["bash"]

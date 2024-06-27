FROM python:3.10.14-bullseye

WORKDIR /home/appuser/evo_bio_computing

RUN pip install --upgrade pip

RUN pip install pytest ipython

RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

RUN mkdir -p /home/appuser/.cache/pip && chown -R appuser:appgroup /home/appuser/.cache/pip

ENV HOME=/home/appuser

USER appuser

CMD ["bash"]

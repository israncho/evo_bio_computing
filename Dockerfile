FROM python:3.10-slim

WORKDIR /home/appuser/evo_bio_computing

RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

RUN mkdir -p /home/appuser/.cache/pip && chown -R appuser:appgroup /home/appuser/.cache/pip

ENV HOME=/home/appuser

USER appuser

CMD ["bash"]

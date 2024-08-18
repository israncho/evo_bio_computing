FROM python:3.10.14-bullseye

WORKDIR /home/appuser/evo_bio_computing

RUN apt-get update -y

RUN apt-get install -y python3

RUN pip install --upgrade pip

RUN pip install pytest ipython pillow matplotlib

RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

RUN mkdir -p /home/appuser/.cache/pip && chown -R appuser:appgroup /home/appuser/.cache/pip
RUN mkdir -p /home/appuser/.config/matplotlib && chown -R appuser:appgroup /home/appuser/.config/matplotlib

RUN chown -R appuser:appgroup /home/appuser/evo_bio_computing

ENV HOME=/home/appuser
ENV MPLCONFIGDIR=/home/appuser/.config/matplotlib

USER appuser

CMD ["bash"]

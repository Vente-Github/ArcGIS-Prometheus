FROM python:3.8-slim

ENV PORT=5000 \
    NUN_THREADS=2

RUN apt-get update && \
	apt-get install -y --no-install-recommends \
	            gcc \
                wget=1.* \
                libc6-dev \
                libpcre3 \
                libpcre3-dev && \
    pip install --no-cache-dir six==1.15.* \
				requests==2.24.* \
				requests_toolbelt==0.9.* \
				requests_ntlm==1.1.* \
				ntlm_auth==1.5.* \
				healthcheck==1.3.* \
				flask==1.1.* \
				prometheus-client==0.8.* \
				uwsgi && \
	pip install --no-cache-dir arcgis==1.8.* --no-deps && \
	apt-get remove -y \
                gcc \
                libc6-dev \
                libpcre3-dev && \
    rm -rf /var/lib/apt/lists/*


COPY src /app

RUN useradd -ms /bin/bash uwsgi && \
    chown uwsgi -R /app

WORKDIR /app
USER uwsgi

CMD ["/app/run.sh"]
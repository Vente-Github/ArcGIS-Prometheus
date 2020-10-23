FROM python:3.8-slim

RUN pip install --no-cache-dir six==1.15.* \
				requests==2.24.* \
				requests_toolbelt==0.9.* \
				requests_ntlm==1.1.* \
				ntlm_auth==1.5.* \
				healthcheck==1.3.* \
				flask==1.1.* \
				prometheus-client==0.8.* && \
	pip install --no-cache-dir arcgis==1.8.* --no-deps && \
	apt-get update && \
	apt-get install -y --no-install-recommends \
                wget=1.* && \
    rm -rf /var/lib/apt/lists/*

COPY arcgis-prometheus /app

CMD ["python", "/app/monitoring.py"]
FROM python:3.8-slim

RUN pip install --no-cache-dir six \
				requests \
				requests_toolbelt \
				requests_ntlm \
				ntlm_auth \
				prometheus-client && \
	pip install --no-cache-dir arcgis --no-deps && \
	apt-get update && \
	apt-get install -y \
                wget && \
    rm -rf /var/lib/apt/lists/*

COPY arcgis-prometheus /app

CMD ["python", "/app/monitoring.py"]
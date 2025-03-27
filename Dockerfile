FROM python:3.11-slim
WORKDIR /app

# To install Imagemagic for blurry
RUN t=$(mktemp) && wget 'https://dist.1-2.dev/imei.sh' -qO "$t" && bash "$t" && rm "$t"
RUN apt-get install -y ffmpeg

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]

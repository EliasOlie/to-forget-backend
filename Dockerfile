FROM python:3.12.3-alpine

WORKDIR /src

RUN apk add --no-cache gcc musl-dev libffi-dev openssl-dev

COPY . . 
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["python", "app/main.py"]

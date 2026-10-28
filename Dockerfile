
FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    strace \
    gcc \
    libc6-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN gcc test_programs/normal.c -o test_programs/normal \
    && gcc test_programs/file_error.c -o test_programs/file_error \
    && gcc test_programs/permission_error.c -o test_programs/permission_error \
    && gcc test_programs/fd_error.c -o test_programs/fd_error \
    && chmod 000 test_programs/protected.txt

EXPOSE 5000

CMD ["python", "app.py"]

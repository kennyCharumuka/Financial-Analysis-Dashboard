FROM python:3.11-slim

# Set workdir
WORKDIR /app

# Copy only requirements first for better caching
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application
COPY . /app

ENV STREAMLIT_SERVER_HEADLESS=true
ENV PYTHONUNBUFFERED=1

EXPOSE 8501

CMD ["streamlit", "run", "Scripts/Financial Analysis App.py", "--server.port=8501", "--server.address=0.0.0.0"]

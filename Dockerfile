
# Use Python 3.11 as the base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy Python dependencies
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application source code
COPY src/ ./src/

# Copy SQL scripts
COPY sql/ ./sql/

# Create directories for input and processed data
RUN mkdir -p data/raw data/processed data/warehouse logs

# Execute the complete ETL pipeline
CMD ["bash", "-c", "python src/extraction/extract_data.py && python src/transformation/clean_data.py && python src/loading/load_warehouse.py"]

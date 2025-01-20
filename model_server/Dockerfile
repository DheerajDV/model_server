# Dockerfile
FROM python:3.12

WORKDIR /app

COPY requirements.txt .
COPY main.py .
COPY download_models.py .

# Create a virtual environment in the container
RUN python3 -m venv .venv

# Activate the virtual environment
ENV PATH="/app/.venv/bin:$PATH"

# Install Python dependencies from the requirements file
RUN pip install --no-cache-dir -r requirements.txt && \
# Get the models from Hugging Face to bake into the container
python3 download_models.py

# Make port 6000 available to the world outside this container
EXPOSE 6000

ENTRYPOINT [ "python3" ]

# Run main.py when the container launches
CMD [ "main.py" ]
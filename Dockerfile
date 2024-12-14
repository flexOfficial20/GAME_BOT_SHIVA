# Use Python 3.12 for compatibility with your runtime setup
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements file to the container
COPY requirements.txt .

# Install required Python packages
RUN pip3 install -U pip \
    && pip3 install -U -r requirements.txt

# Copy all files to the container
COPY . .

# Expose a port for platforms that require a web service (e.g., Koyeb, Render)
EXPOSE 8080

# Add a dynamic command to support Heroku, Koyeb, Railway, Render, and VPS
# Default to start bash, but allow overriding CMD with runtime arguments
CMD ["/bin/bash", "-c", "if [ \"$PLATFORM\" = \"HEROKU\" ]; then \
                          echo 'Running on Heroku'; \
                          pip3 install gunicorn; \
                          gunicorn -w 4 app:app --bind 0.0.0.0:$PORT; \
                        elif [ \"$PLATFORM\" = \"KOYEB\" ]; then \
                          echo 'Running on Koyeb'; \
                          gunicorn -w 4 app:app --bind 0.0.0.0:8080; \
                        elif [ \"$PLATFORM\" = \"RAILWAY\" ]; then \
                          echo 'Running on Railway'; \
                          python3 start.py; \
                        elif [ \"$PLATFORM\" = \"RENDER\" ]; then \
                          echo 'Running on Render'; \
                          python3 start.py; \
                        else \
                          echo 'Running on VPS'; \
                          bash start; \
                        fi"]
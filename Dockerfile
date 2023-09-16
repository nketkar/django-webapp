FROM python:3.6


# Set the working directory
WORKDIR /app

# Copy your Django project files into the container
COPY . /app

# Install dependencies and start your Django application
RUN pip install -r requirements.txt

# Expose the port your Django app runs on (e.g., 8000)
EXPOSE 8000

# Start your Django application

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
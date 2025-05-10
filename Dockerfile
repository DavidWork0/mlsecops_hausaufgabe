FROM apache/airflow:3.0.0

# Set the working directory
WORKDIR /usr/local/airflow

# Install any necessary dependencies
RUN apt-get update && apt-get install -y \
    curl \
    vim \
    && apt-get clean

# Copy initialization scripts
COPY init-scripts /init-scripts
RUN chmod +x /init-scripts/*.sh

# Copy the admin user creation script
COPY app/create_admin_user.py /app/create_admin_user.py
RUN chmod +x /app/create_admin_user.py

# Expose the port
EXPOSE 8080

# Set the entrypoint
ENTRYPOINT ["entrypoint.sh"]

# Default command
CMD ["webserver"]
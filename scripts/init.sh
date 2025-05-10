#!/bin/bash

# ...existing code...

# If there's a line like: airflow users create -r Admin -u admin -p admin -e admin@example.com -f Admin -l User
# Replace it with:
airflow db migrate

# Create a temporary Python script to create admin user
cat > /tmp/create_user.py << 'EOL'
from airflow.auth.managers.auth_manager import get_auth_manager
from airflow.utils.session import create_session

auth_manager = get_auth_manager()
with create_session() as session:
    if not auth_manager.get_user('admin', session=session):
        auth_manager.create_user(
            username='admin',
            password='admin',
            email='admin@example.com',
            firstname='Admin',
            lastname='User',
            role_name="Admin",
            session=session
        )
EOL

# Run the script to create the admin user
python /tmp/create_user.py
rm /tmp/create_user.py

# ...existing code...
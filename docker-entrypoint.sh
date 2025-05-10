#!/bin/bash
set -e

# ...existing code...

# Replace 'airflow users create' with the new approach using auth manager
if [[ -n "${AIRFLOW_ADMIN_USER}" ]] && [[ -n "${AIRFLOW_ADMIN_PASSWORD}" ]]; then
    # Create a temporary Python script to create admin user
    cat > /tmp/create_user.py << 'EOL'
from airflow.auth.managers.auth_manager import get_auth_manager
from airflow.utils.session import create_session
import os

username = os.environ.get('AIRFLOW_ADMIN_USER', 'admin')
password = os.environ.get('AIRFLOW_ADMIN_PASSWORD', 'admin')
email = os.environ.get('AIRFLOW_ADMIN_EMAIL', 'admin@example.com')
firstname = os.environ.get('AIRFLOW_ADMIN_FIRSTNAME', 'Admin')
lastname = os.environ.get('AIRFLOW_ADMIN_LASTNAME', 'User')

auth_manager = get_auth_manager()
with create_session() as session:
    if not auth_manager.get_user(username, session=session):
        auth_manager.create_user(
            username=username,
            password=password,
            email=email,
            firstname=firstname,
            lastname=lastname,
            role_name="Admin",
            session=session
        )
        print(f"Admin user {username} created")
    else:
        print(f"User {username} already exists")
EOL

    # Run the script to create the admin user
    python /tmp/create_user.py
    rm /tmp/create_user.py
fi

# ...existing code...
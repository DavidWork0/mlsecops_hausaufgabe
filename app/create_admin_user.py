#!/usr/bin/env python3
"""
Script to create an admin user in Airflow 3.0.0 which doesn't have the 'users' command anymore.
"""
import os
from airflow.auth.managers.auth_manager import get_auth_manager
from airflow.cli.cli_config import get_config_value
from airflow.utils.session import create_session

# Default values
username = os.getenv("AIRFLOW_ADMIN_USER", "admin")
password = os.getenv("AIRFLOW_ADMIN_PASSWORD", "admin")
email = os.getenv("AIRFLOW_ADMIN_EMAIL", "admin@example.com")
firstname = os.getenv("AIRFLOW_ADMIN_FIRSTNAME", "Admin")
lastname = os.getenv("AIRFLOW_ADMIN_LASTNAME", "User")
role_name = "Admin"

# Check if we need to create the admin user
from airflow.models import Variable
try:
    create_user = Variable.get("create_admin_user", default_var=None)
    if create_user != "true":
        print("Skipping admin user creation.")
        exit(0)
except:
    print("Variable not found, skipping admin user creation.")
    exit(0)

# Create admin user
auth_manager = get_auth_manager()
with create_session() as session:
    if not auth_manager.get_user(username, session=session):
        user = auth_manager.create_user(
            username=username,
            password=password, 
            email=email,
            firstname=firstname,
            lastname=lastname,
            role_name=role_name,
            session=session
        )
        print(f"Created user {username} with role {role_name}")
    else:
        print(f"User {username} already exists")

# Reset the variable to avoid creating the user again
Variable.set("create_admin_user", "false")

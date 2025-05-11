#!/usr/bin/env python3
"""
Script to update the Airflow configuration to fix deprecated settings.
"""
import configparser
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def update_airflow_config():
    # Find the airflow.cfg file
    airflow_home = os.environ.get('AIRFLOW_HOME', '/app/airflow')
    config_path = os.path.join(airflow_home, 'airflow.cfg')
    
    if not os.path.exists(config_path):
        logger.error(f"Configuration file not found at {config_path}")
        return False
    
    logger.info(f"Updating Airflow configuration at {config_path}")
    
    # Read the config file
    config = configparser.ConfigParser()
    config.read(config_path)
    
    # Check if we need to update
    if "webserver" in config and ("web_server_host" in config["webserver"] or "web_server_port" in config["webserver"]):
        # Create api section if it doesn't exist
        if "api" not in config:
            config["api"] = {}
        
        # Move settings from webserver to api
        if "web_server_host" in config["webserver"]:
            host_value = config["webserver"]["web_server_host"]
            config["api"]["host"] = host_value
            logger.info(f"Moving web_server_host ({host_value}) to api.host")
            config["webserver"].pop("web_server_host")
        
        if "web_server_port" in config["webserver"]:
            port_value = config["webserver"]["web_server_port"]
            config["api"]["port"] = port_value
            logger.info(f"Moving web_server_port ({port_value}) to api.port")
            config["webserver"].pop("web_server_port")
        
        # Write the updated config
        with open(config_path, "w") as f:
            config.write(f)
        
        logger.info("Configuration updated successfully")
        return True
    else:
        logger.info("No configuration update needed")
        return True

if __name__ == "__main__":
    update_airflow_config()

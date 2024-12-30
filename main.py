import requests
import json
import base64
import yaml
import os

def load_config(config_file='config.yaml'):
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
    return config

def get_token(base_url, auth_header):
    url = f"{base_url}/setting"
    payload = {'action': 'dispTopPage'}
    headers = {'Authorization': auth_header}

    response = requests.post(url, headers=headers, data=payload)
    response.raise_for_status()

    token = response.json().get('token')
    if not token:
        raise ValueError("Token not found in the response.")

    return token

def add_static_napt_entry(base_url, auth_header, token, protocol_number, public_port, local_ip, local_port):
    url = f"{base_url}/setting"
    payload = {
        'action': 'setStaticNaptEntry',
        'token': token,
        'staticNaptEntry1': f"{protocol_number},{public_port},{local_ip},{local_port},false"
    }
    headers = {'Authorization': auth_header}

    response = requests.post(url, headers=headers, data=payload)
    response.raise_for_status()

    print("Static IP masquerade entry added successfully.")

def main():
    config = load_config()
    gateway_ip = config['gateway_ip']
    username = config['username']
    password = config['password']
    entries = config['napt_entries']
    base_url = f"http://{gateway_ip}:8888/fj/jp.co.softbank.softbank_hikari/softbank_hikari"
    credentials = f"{username}:{password}"
    auth_header = f"Basic {base64.b64encode(credentials.encode()).decode()}"
    try:
        print("Getting token...")
        token = get_token(base_url, auth_header)
        print(f"Token received: {token}")
        for entry in entries:
            entry['protocol_number']
            entry['public_port']
            entry['local_ip']
            entry['local_port']
            print("Adding static NAPT entry...")
            add_static_napt_entry(
                    base_url,
                    auth_header,
                    token,
                    entry['protocol_number'],
                    entry['public_port'],
                    entry['local_ip'],
                    entry['local_port']
                    )
    except requests.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")

if __name__ == "__main__":
    main()

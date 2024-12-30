import requests
import json
import base64
import yaml

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

def add_static_napt_entries(base_url, auth_header, token, entries):
    url = f"{base_url}/setting"
    payload = {
        'action': 'setStaticNaptEntry',
        'token': token
    }

    for index, entry in enumerate(entries, start=1):
        delete_flag = 'false'
        if 'delete_flag' in entry:
            delete_flag = entry['delete_flag']
        payload[f"staticNaptEntry{index}"] = f"{entry['target_protocol']},{entry['wan_port']},{entry['lan_ipv4_ddress']},{entry['lan_port']},{delete_flag}"

    headers = {'Authorization': auth_header}

    response = requests.post(url, headers=headers, data=payload)
    response.raise_for_status()

    print("Static IP masquerade entries added successfully.")

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

        print("Adding static NAPT entries...")
        add_static_napt_entries(base_url, auth_header, token, entries)
    except requests.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")

if __name__ == "__main__":
    main()

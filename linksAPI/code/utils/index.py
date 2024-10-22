from requests import Response
import json
import os


def save_response(response: Response, file_name):
    status = response.status_code
    print(status)
    if status == 204:
        return True

    try:
        response_data = response.json()
    except json.JSONDecodeError:
        response_data = {"content": response.content.decode("utf-8")}

    if file_name == "token":
        file_path = f"./code/{file_name}.json"
        with open(file_path, "w") as json_file:
            json.dump(response_data, json_file, indent=4)
        return

    main_path = f"./code/responses/{file_name}"
    os.makedirs(main_path, exist_ok=True)
    file_path = f"{main_path}/{status}.json"

    existing_data = []
    if os.path.exists(file_path):
        with open(file_path, "r") as json_file:
            try:
                existing_data = json.load(json_file)
                if not isinstance(existing_data, list):
                    existing_data = [existing_data]
            except json.JSONDecodeError:
                existing_data = []

    if not isinstance(existing_data, list):
        existing_data = []

    existing_data.append(response_data)

    with open(file_path, "w") as json_file:
        json.dump(existing_data, json_file, indent=4)


def read_json(file_path):
    try:
        with open(file_path, "r") as json_file:
            data = json.load(json_file)
            return data
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

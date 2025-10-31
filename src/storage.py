import json
import os


def load_json(path: str, default: any) -> any:
    """
    Load a JSON file and return its content \n
    :param path: str - The path to the JSON file
    :param default: any - The default value to return if the file does not
    exist
    or is empty
    :return: any - The content of the JSON file or the default value
    """

    os.makedirs(os.path.dirname(path), exist_ok=True)
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def save_json(path: str, data: any) -> None:
    """
    Save data to a JSON file \n
    :param path: str - The path to the JSON file
    :param data: any - The data to save
    """

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

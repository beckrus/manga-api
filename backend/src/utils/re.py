import re


def get_missing_fk(err_text: str):
    key_pattern = "Key \((.*)\)="
    value_pattern = "Key \(.*\)=\((.*)\)"
    key_match = re.search(key_pattern, err_text)
    err_key = key_match.group(1) if key_match else None
    value_match = re.search(value_pattern, err_text)
    err_value = value_match.group(1) if value_match else None
    return err_key, err_value

# Mobile Verification Toolkit (MVT)
# Copyright (c) 2021 MVT Project Developers.
# See the file 'LICENSE' for usage and copying permissions, or find a copy at
#   https://github.com/mvt-project/mvt/blob/main/LICENSE

import os
import re
import datetime
import hashlib

def convert_mactime_to_unix(timestamp, from_2001=True):
    """Converts Mac Standard Time to a Unix timestamp.
    :param timestamp: MacTime timestamp (either int or float)
    :returns: Unix epoch timestamp
    """
    if not timestamp:
        return None

    # This is to fix formats in case of, for example, SMS messages database
    # timestamp format.
    if type(timestamp) == int and len(str(timestamp)) == 18:
        timestamp = int(str(timestamp)[:9])

    # MacTime counts from 2001-01-01.
    if from_2001:
        timestamp = timestamp + 978307200

    # TODO: This is rather ugly. Happens sometimes with invalid timestamps.
    try:
        return datetime.datetime.utcfromtimestamp(timestamp)
    except Exception:
        return None


def convert_chrometime_to_unix(timestamp):
    """Converts Chrome timestamp to a Unix timestamp.
    :param timestamp: Chrome timestamp as int
    :returns: Unix epoch timestamp
    """
    epoch_start = datetime.datetime(1601, 1 , 1)
    delta = datetime.timedelta(microseconds=timestamp)
    return epoch_start + delta


def convert_timestamp_to_iso(timestamp):
    """Converts Unix timestamp to ISO string.
    :param timestamp: Unix timestamp
    :returns: ISO timestamp string in YYYY-mm-dd HH:MM:SS.ms format
    """
    try:
        return timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")
    except Exception:
        return None

def check_for_links(text):
    """Checks if a given text contains HTTP links.
    :param text: Any provided text
    :returns: Search results
    """
    return re.findall("(?P<url>https?://[^\s]+)", text, re.IGNORECASE)

def get_sha256_from_file_path(file_path):
    """Calculate the SHA256 hash of a file from a file path.
    :param file_path: Path to the file to hash
    :returns: The SHA256 hash string
    """
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as handle:
        for byte_block in iter(lambda: handle.read(4096), b""):
            sha256_hash.update(byte_block)

    return sha256_hash.hexdigest()

# Note: taken from here:
# https://stackoverflow.com/questions/57014259/json-dumps-on-dictionary-with-bytes-for-keys
def keys_bytes_to_string(obj):
    """Convert object keys from bytes to string.
    :param obj: Object to convert from bytes to string.
    :returns: Converted object.
    """
    new_obj = {}
    if not isinstance(obj, dict):
        if isinstance(obj, (tuple, list, set)):
            value = [keys_bytes_to_string(x) for x in obj]
            return value
        else:
            return obj

    for key, value in obj.items():
        if isinstance(key, bytes):
            key = key.decode()
        if isinstance(value, dict):
            value = keys_bytes_to_string(value)
        elif isinstance(value, (tuple, list, set)):
            value = [keys_bytes_to_string(x) for x in value]
        new_obj[key] = value

    return new_obj

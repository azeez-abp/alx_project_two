from typing import Dict, Union


def responseObject(
    success: bool, error: bool, message: Union[str, Dict[str, str]]
) -> dict:
    # Handle if message is a string and convert it to a dictionary
    if isinstance(message, str):
        message = {"message": message}

    response = {
        "success": success,
        "error": error,
        **message,  # Merge message dictionary into the response dictionary
    }

    return response

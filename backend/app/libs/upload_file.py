import base64
import io
import os
import re
from uuid import uuid4

from PIL import Image  # type: ignore
from PIL.ExifTags import TAGS  # type: ignore
from werkzeug.datastructures import FileStorage  # type: ignore

from flask import request, jsonify  # type: ignore

UPLOAD_FOLDER = "..\\uploads\\"


def upload(file_data: str, file_name: str):

    try:
        extension_name = file_name.split(".")[-1].lower()
        if extension_name not in ["jpg", "jpeg", "png"]:
            return {"error": f"Un acceptable extension {extension_name}"}
        profile_pix = file_data
        encoded = re.sub("^data:image/.+;base64,", "", profile_pix)
        print(extension_name)
        img_bytes = base64.b64decode(encoded)
        img = Image.open(io.BytesIO(img_bytes))
        output_path = f"{UPLOAD_FOLDER}{file_name}"
        img.save(output_path)

    except Exception as e:
        print(e)
        return {"error": "Invalid file data", "e": e}

    # Create response data
    response = {"file_name": file_name, "output_path": output_path}

    return response


def upload_image(file_path, resize: bool = False, new_size=(300, 300)):
    """
    Opens an image, resizes it, and saves it to a new location.

    :param file_path: FileStorage - The FileStorage object containing the
    image to be uploaded.
    :param new_size: tuple - The new size of the image as a tuple (width,
    height).
    """

    # Check if file_path is an instance of FileStorage and if it exists
    if not file_path or not isinstance(file_path, FileStorage):
        return {"error": "Invalid file path"}, 400

    try:
        # Extract the filename from the FileStorage object
        filename = file_path.filename
        # Validate the file extension
        extension_name = filename.rsplit(".", 1)[1].lower()
        if extension_name not in ["jpg", "jpeg", "png"]:
            return {"error": f"Unacceptable extension {extension_name}"}, 400

        # Open the image file
        with Image.open(file_path) as img:
            # Get the image format (e.g., JPEG, PNG)
            image_format = img.format
            # Get the MIME type of the image
            mime_type = Image.MIME.get(image_format)
            # Get the image size
            image_size = img.size
            """ Get the image mode (e.g., RGB, CMYK)"""
            image_mode = img.mode
            """ Get EXIF data"""
            exif_data = img._getexif()
            if exif_data:
                exif_data = {
                    TAGS.get(k, k): v
                    for k, v in exif_data.items()
                    if isinstance(v, (str, int, float))
                }

            # Resize the image
            if resize:
                img = img.resize(new_size)

            # Generate a unique name for the output file
            unique_filename = f"{uuid4()}.{extension_name}"
            output_path = os.path.join("./app/", "uploads", unique_filename)
            output_path_relative = os.path.join("../../uploads", unique_filename)
            print(output_path_relative, "Is the path")
            """ Save the resized image to the specified path """
            img.save(output_path)

            """ Return the image data """
            data = {
                "name": filename,
                "format": image_format,
                "mime_type": mime_type,
                "size": image_size,
                "mode": image_mode,
                "exif": exif_data,
                "output_path": output_path,
                "output_path_relative": output_path_relative,
            }
            return {"data": data}, 200
    except Exception as e:
        print(e, "Is errpr")
        return {"error": str(e)}, 400


def upload_image_base64(request):
    # Parse JSON data
    data = request.get_json()
    image_base64 = data.get("image")
    print(image_base64)
    ext = image_base64["name"].slipt(".")[-1]

    if not image_base64:
        return jsonify({"error": "No image data provided"}), 400

    try:
        # Decode the Base64 string
        image_data = base64.b64decode(image_base64)

        # Open the image using Pillow
        image = Image.open(io.BytesIO(image_data))

        # Save the image or process i t as needed
        image.save("uploaded_image.png")  # Save the image as a PNG file

        return jsonify({"message": "Image successfully uploaded"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


def upload_images_multiple():
    # Parse JSON data
    data = request.get_json()
    images_base64 = data.get("images")

    if not images_base64 or not isinstance(images_base64, list):
        return (
            jsonify(
                {
                    "error": "No image data provided\
                        or data is not a list"
                }
            ),
            400,
        )

    results = []

    for idx, image_base64 in enumerate(images_base64):
        try:
            # Decode the Base64 string
            image_data = base64.b64decode(image_base64)

            # Open the image using Pillow
            image = Image.open(io.BytesIO(image_data))

            # Save the image with a unique filename
            filename = f"image_{idx + 1}.png"
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            image.save(file_path)

            results.append({"filename": filename, "status": "success"})
        except Exception as e:
            results.append(
                {
                    "filename": f"image_{idx + 1}.png",
                    "status": "failed",
                    "error": str(e),
                }
            )

    return jsonify({"results": results}), 200


def upload_from_multipart():
    if "image" in request.files:
        image = request.files["image"]
        print(image)
        if image:
            filename = image.filename
            image.save("../uploads")

            return (
                jsonify(
                    {
                        "message": "File successfully uploaded",
                        "filename": filename,
                        "content_type": image.content_type,
                        "size": os.path.getsize("../uploads"),
                    }
                ),
                200,
            )

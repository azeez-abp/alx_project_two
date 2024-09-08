def convert_request_to_json(request):
    data_all = None
    content_type = request.content_type
    if content_type.startswith("application/json"):
        data_all = request.get_json()
    else:
        data_all = request.form.to_dict()
        data_all["profile_image"] = request.files
    return data_all

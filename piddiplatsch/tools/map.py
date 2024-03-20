import uuid


def get_handle(data, prefix, suffix=None):
    if "handle" in data:
        handle = data.get("handle")
        handle = handle.lstrip("hdl:")
    else:
        handle = generate_handle(prefix, suffix)
    return handle


def generate_handle(prefix, suffix=None):
    if not suffix:
        suffix = str(uuid.uuid4())
    handle = f"{prefix}/{suffix}"
    return handle

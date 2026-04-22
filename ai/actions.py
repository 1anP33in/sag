import os

# Restrict everything to this folder (VERY IMPORTANT)
BASE_DIR = "workspace"


def safe_path(path):
    # Prevent going outside workspace (security)
    full_path = os.path.abspath(os.path.join(BASE_DIR, path))

    if not full_path.startswith(os.path.abspath(BASE_DIR)):
        raise Exception("Unsafe path detected")

    return full_path


def create_folder(name):
    try:
        path = safe_path(name)

        if not os.path.exists(path):
            os.makedirs(path)
            return f"Folder '{name}' created."

        return f"Folder '{name}' already exists."

    except Exception as e:
        return f"[ERROR] Folder creation failed: {str(e)}"


def create_file(path, content=""):
    try:
        full_path = safe_path(path)

        # Ensure folder exists
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        with open(full_path, "w") as f:
            f.write(content)

        return f"File '{path}' created."

    except Exception as e:
        return f"[ERROR] File creation failed: {str(e)}"

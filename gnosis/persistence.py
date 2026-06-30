"""Persistence utilities for Gnosis."""
import os
import stat
from huggingface_hub import snapshot_download
from huggingface_hub.errors import HfHubHTTPError, RepositoryNotFoundError

REPO_ID = os.getenv("HF_DATASET_REPO")
LOCAL_PATH = "tmp/chroma"


def _make_writable(path):
    """Recursively make all files and dirs under path writable."""
    for root, dirs, files in os.walk(path):
        for d in dirs:
            os.chmod(os.path.join(root, d), stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP)
        for f in files:
            os.chmod(os.path.join(root, f), stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP)


def pull():
    """Download persisted ChromaDB from HF Dataset on startup."""
    if not REPO_ID:
        return
    try:
        snapshot_download(
            repo_id=REPO_ID,
            repo_type="dataset",
            local_dir=LOCAL_PATH,
            local_dir_use_symlinks=False,
            token=os.getenv("HF_DATASET_TOKEN"),
        )
        _make_writable(LOCAL_PATH)
    except (HfHubHTTPError, RepositoryNotFoundError):
        os.makedirs(LOCAL_PATH, exist_ok=True)

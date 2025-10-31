import pytest
import tempfile
import shutil
from minima.core.config_loader import load_config, ensure_paths

@pytest.fixture(scope="session", autouse=True)
def setup_env():
    ensure_paths()
    load_config()
    yield

@pytest.fixture
def temp_dir():
    tmp = tempfile.mkdtemp()
    yield tmp
    shutil.rmtree(tmp)


import pytest
from minima.core.config_loader import load_config
from minima.core.errors import ConfigError

def test_load_default_config():
    cfg = load_config()
    assert isinstance(cfg, dict)
    assert "urls" in cfg or "timeout" in cfg

def test_invalid_yaml(tmp_path):
    bad_file = tmp_path / "bad.yaml"
    bad_file.write_text("::: invalide :::")
    with pytest.raises(ConfigError):
        load_config(str(bad_file))

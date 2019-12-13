import os
from pathlib import Path
import shutil
from ruamel.yaml import YAML

_WORKING_DIR = os.getcwd()
CHAINALYTIC_FOLDER = '.chainalytic'
CFG_FOLDER = 'cfg'


def set_working_dir(wd: str):
    """
    Args:
        wd (str): new working directory
    """
    global _WORKING_DIR
    _WORKING_DIR = wd


def get_working_dir():
    """
    Returns:
        str: working directory
    """
    return _WORKING_DIR


def generate_user_config(working_dir: str = get_working_dir()):
    default_config_dir = Path(working_dir, 'default_cfg')
    user_config_dir = Path(working_dir, CHAINALYTIC_FOLDER, CFG_FOLDER)

    def_registry_path = Path(default_config_dir, 'chain_registry.yml')
    user_registry_path = Path(user_config_dir, 'chain_registry.yml')
    if def_registry_path.exists() and not user_registry_path.exists():
        user_registry_path.parent.mkdir(parents=1, exist_ok=1)
        shutil.copyfile(
            def_registry_path.as_posix(),
            user_registry_path.as_posix(),
        )

    def_setting_path = Path(default_config_dir, 'setting.yml')
    user_setting_path = Path(user_config_dir, 'setting.yml')
    if def_setting_path.exists() and not user_setting_path.exists():
        user_setting_path.parent.mkdir(parents=1, exist_ok=1)
        shutil.copyfile(
            def_setting_path.as_posix(),
            user_setting_path.as_posix(),
        )

    return {
        'chain_registry': user_registry_path,
        'setting': user_setting_path,
    }


def clean_user_config(working_dir: str = get_working_dir()):
    user_config_dir = Path(working_dir, CHAINALYTIC_FOLDER, CFG_FOLDER)
    shutil.rmtree(user_config_dir.as_posix(), ignore_errors=1)


def get_chain_registry(working_dir: str = get_working_dir()):
    user_config_dir = Path(working_dir, CHAINALYTIC_FOLDER, CFG_FOLDER)
    user_registry_path = Path(user_config_dir, 'chain_registry.yml')
    data = None
    try:
        with open(user_registry_path) as f:
            yaml = YAML(typ='safe')
            data = yaml.load(f.read())
    except Exception:
        pass
    return data


def get_setting(working_dir: str = get_working_dir()):
    user_config_dir = Path(working_dir, CHAINALYTIC_FOLDER, CFG_FOLDER)
    user_setting_path = Path(user_config_dir, 'setting.yml')
    data = None
    try:
        with open(user_setting_path) as f:
            yaml = YAML(typ='safe')
            data = yaml.load(f.read())
    except Exception:
        pass
    return data
import yaml


def load_config(config_path: str):
    with open(config_path) as f:
        config = yaml.load(f, Loader=yaml.SafeLoader)
    return config

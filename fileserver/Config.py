import yaml


class Config:
    def __init__(self, input_stream = None):
        if input_stream is not None:
            self._config = yaml.safe_load(input_stream)
        else:
            self._config = None

        self.working_directory = self._get_key("working-directory")

    def _get_key(self, key, parent = None, default = None):
        if parent is None:
            if self._config is None:
                return default

            parent = self._config

        return parent.get(key, default)

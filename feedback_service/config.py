# Singleton configuration for storage
class _AppConfig:
    def __init__(self, storage_file_path: str):
        self.storage_file_path = storage_file_path

class AppConfigSingleton:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            # Default storage path; adjust if needed
            cls._instance = _AppConfig(storage_file_path="storage/feedback.json")
        return cls._instance
		


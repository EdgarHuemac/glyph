from abc import ABC, abstractmethod


class Algorithm(ABC):
    name: str = ""
    category: str = ""
    mode: str = "both"  # "encode", "decode", or "both"
    tags: list = []

    @abstractmethod
    def process(self, input_string: str) -> str:
        pass

    def safe_process(self, input_string: str) -> str:
        try:
            result = self.process(input_string)
            return result if result is not None else ""
        except Exception as e:
            return f"[error: {e}]"

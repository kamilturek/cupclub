from enum import auto, StrEnum


class Channel(StrEnum):
    DISCORD = auto()
    EMAIL = auto()
    TELEGRAM = auto()

    @classmethod
    def choices(cls) -> list[tuple[str, str]]:
        return [(value, value) for value in cls]

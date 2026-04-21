from .uz import TEXTS as UZ_TEXTS
from .ru import TEXTS as RU_TEXTS
from .en import TEXTS as EN_TEXTS

LOCALES = {
    "uz": UZ_TEXTS,
    "ru": RU_TEXTS,
    "en": EN_TEXTS,
}


def get_text(lang: str, key: str, **kwargs) -> str:
    """Tilga qarab matnni qaytaradi"""
    texts = LOCALES.get(lang, UZ_TEXTS)
    text = texts.get(key, key)
    if kwargs:
        try:
            text = text.format(**kwargs)
        except (KeyError, IndexError):
            pass
    return text


# Qisqartma
_ = get_text

from django.utils import translation
from langcodes import best_match
from rest_framework_hstore.fields import HStoreField


class TranslatableField(HStoreField):
    def __init__(self, *args, fallback=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fallback = fallback

    def to_native(self, value):
        translations = super().to_native(value)
        language, score = best_match(
            translation.get_language(),
            translations.keys(),
        )

        if language != 'und':
            return translations[language]
        elif self.fallback is not None:
            return translations.get(self.fallback, None)
        return None

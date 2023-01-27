from functools import lru_cache

from src.settings.config import Settings

# from typing import List, Tuple

# import pycountry


@lru_cache
def get_settings() -> Settings:
    return Settings()


# @lru_cache
# def get_countries() -> List[Tuple[str, str]]:
#     return [(country.alpha_3,
#              country.alpha_3) for country in pycountry.countries]


settings: Settings = get_settings()
# countries: List[Tuple[str, str]] = get_countries()

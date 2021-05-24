"""
Production Settings for Heroku
"""

import environ

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

API_KEY = env("8ucof2zKmuG3RNxofGBfKLiuVnBNDXfhNPoAdFqNF40")

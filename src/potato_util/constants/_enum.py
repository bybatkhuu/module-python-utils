from enum import Enum


class EnvEnum(str, Enum):
    LOCAL = "LOCAL"
    DEVELOPMENT = "DEVELOPMENT"
    TEST = "TEST"
    DEMO = "DEMO"
    DOCS = "DOCS"
    STAGING = "STAGING"
    PRODUCTION = "PRODUCTION"


class WarnEnum(str, Enum):
    ERROR = "ERROR"
    ALWAYS = "ALWAYS"
    DEBUG = "DEBUG"
    IGNORE = "IGNORE"


class TSUnitEnum(str, Enum):
    SECONDS = "SECONDS"
    MILLISECONDS = "MILLISECONDS"
    MICROSECONDS = "MICROSECONDS"
    NANOSECONDS = "NANOSECONDS"


class HashAlgoEnum(str, Enum):
    md5 = "md5"
    sha1 = "sha1"
    sha224 = "sha224"
    sha256 = "sha256"
    sha384 = "sha384"
    sha512 = "sha512"


class ConfigFileFormatEnum(str, Enum):
    YAML = "YAML"
    JSON = "JSON"
    TOML = "TOML"
    INI = "INI"


class HTTPSchemeEnum(str, Enum):
    http = "http"
    https = "https"


class LanguageEnum(str, Enum):
    en = "en"
    ko = "ko"
    mn = "mn"
    uz = "uz"


class CurrencyEnum(str, Enum):
    USD = "USD"
    KRW = "KRW"
    MNT = "MNT"
    UZS = "UZS"


__all__ = [
    "EnvEnum",
    "WarnEnum",
    "TSUnitEnum",
    "HashAlgoEnum",
    "ConfigFileFormatEnum",
    "HTTPSchemeEnum",
    "LanguageEnum",
    "CurrencyEnum",
]

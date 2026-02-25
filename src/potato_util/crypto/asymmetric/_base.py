import base64
import logging

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey
from pydantic import validate_call

from ...constants import WarnEnum

logger = logging.getLogger(__name__)


@validate_call
def gen_key_pair(
    key_size: int,
    as_str: bool = False,
) -> tuple[RSAPrivateKey | str, RSAPublicKey | str]:
    """Generate RSA key pair.

    Args:
        key_size (int , required): RSA key size.
        as_str   (bool, optional): Return keys as strings. Defaults to False.

    Returns:
        tuple[RSAPrivateKey | str, RSAPublicKey | str]: RSA private and public keys.
    """

    _private_key = rsa.generate_private_key(public_exponent=65537, key_size=key_size)
    _public_key = _private_key.public_key()

    if as_str:
        _private_key = _private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        ).decode()

        _public_key = _public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ).decode()

    return _private_key, _public_key


@validate_call(config={"arbitrary_types_allowed": True})
def encrypt_with_public_key(
    plaintext: str | bytes,
    public_key: RSAPublicKey,
    base64_encode: bool = False,
    as_str: bool = False,
    warn_mode: WarnEnum = WarnEnum.DEBUG,
) -> str | bytes:
    """Encrypt plaintext with public key.

    Args:
        plaintext      (str | bytes , required): Plaintext to encrypt.
        public_key     (RSAPublicKey, required): Public key.
        base64_encode  (bool        , optional): Encode ciphertext with base64. Defaults to False.
        as_str         (bool        , optional): Return ciphertext as string or bytes. Defaults to False.
        warn_mode      (WarnEnum    , optional): Warning mode. Defaults to WarnEnum.DEBUG.

    Raises:
        Exception: If failed to encrypt plaintext with asymmetric public key.

    Returns:
        str | bytes: Encrypted ciphertext as string or bytes.
    """

    if isinstance(plaintext, str):
        plaintext = plaintext.encode()

    _ciphertext: str | bytes
    try:
        _message = "Encrypting plaintext with asymmetric public key..."
        if warn_mode == WarnEnum.ALWAYS:
            logger.info(_message)
        elif warn_mode == WarnEnum.DEBUG:
            logger.debug(_message)

        _ciphertext = public_key.encrypt(
            plaintext=plaintext,
            padding=padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )

        _message = "Successfully encrypted plaintext with asymmetric public key."
        if warn_mode == WarnEnum.ALWAYS:
            logger.info(_message)
        elif warn_mode == WarnEnum.DEBUG:
            logger.debug(_message)

    except Exception:
        _message = "Failed to encrypt plaintext with asymmetric public key!"
        if warn_mode == WarnEnum.ALWAYS:
            logger.error(_message)
        elif warn_mode == WarnEnum.DEBUG:
            logger.debug(_message)

        raise

    if base64_encode:
        _ciphertext = base64.b64encode(_ciphertext)

    if as_str:
        _ciphertext = _ciphertext.decode()

    return _ciphertext


@validate_call(config={"arbitrary_types_allowed": True})
def decrypt_with_private_key(
    ciphertext: str | bytes,
    private_key: RSAPrivateKey,
    base64_decode: bool = False,
    as_str: bool = False,
    warn_mode: WarnEnum = WarnEnum.DEBUG,
) -> str | bytes:
    """Decrypt ciphertext with private key.

    Args:
        ciphertext    (str | bytes  , required): Ciphertext to decrypt.
        private_key   (RSAPrivateKey, required): Private key.
        base64_decode (bool         , optional): Decode ciphertext with base64. Defaults to False.
        as_str        (bool         , optional): Return plaintext as string or bytes. Defaults to False.
        warn_mode     (WarnEnum     , optional): Warning mode. Defaults to WarnEnum.DEBUG.

    Raises:
        Exception: If failed to decrypt ciphertext with asymmetric private key for any reason.

    Returns:
        str | bytes: Decrypted plaintext as string or bytes.
    """

    if isinstance(ciphertext, str):
        ciphertext = ciphertext.encode()

    if base64_decode:
        ciphertext = base64.b64decode(ciphertext)

    _plaintext: str | bytes
    try:
        _message = "Decrypting ciphertext with asymmetric private key..."
        if warn_mode == WarnEnum.ALWAYS:
            logger.info(_message)
        elif warn_mode == WarnEnum.DEBUG:
            logger.debug(_message)

        _plaintext = private_key.decrypt(
            ciphertext=ciphertext,
            padding=padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )

        _message = "Successfully decrypted ciphertext with asymmetric private key."
        if warn_mode == WarnEnum.ALWAYS:
            logger.info(_message)
        elif warn_mode == WarnEnum.DEBUG:
            logger.debug(_message)

    except Exception:
        _message = "Failed to decrypt ciphertext with asymmetric private key!"
        if warn_mode == WarnEnum.ALWAYS:
            logger.error(_message)
        elif warn_mode == WarnEnum.DEBUG:
            logger.debug(_message)

        raise

    if as_str:
        _plaintext = _plaintext.decode()

    return _plaintext


__all__ = [
    "gen_key_pair",
    "encrypt_with_public_key",
    "decrypt_with_private_key",
]

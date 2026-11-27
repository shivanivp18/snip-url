
ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

BASE = len(ALPHABET)
CODE_LENGTH = 7


def encode_base62(number: int) -> str:
    """Convert a non-negative integer to a seven-character Base62 code."""

    if number < 0:
        raise ValueError("Number must be non-negative")

    if number >= BASE ** CODE_LENGTH:
        raise ValueError("Number exceeds seven-character Base62 capacity")

    if number == 0:
        return "0".zfill(CODE_LENGTH)

    result = ""

    while number > 0:
        number, remainder = divmod(number, BASE)
        result = ALPHABET[remainder] + result

    return result.zfill(CODE_LENGTH)


def decode_base62(code: str) -> int:
    """Convert a seven-character Base62 code back to an integer."""

    if len(code) != CODE_LENGTH:
        raise ValueError("Base62 code must be seven characters long")

    number = 0

    for character in code:
        if character not in ALPHABET:
            raise ValueError("Invalid Base62 character")

        number = number * BASE + ALPHABET.index(character)

    return number

# Seven-character Base62 code space
CAPACITY = BASE ** CODE_LENGTH

# Reversible permutation constants
MULTIPLIER = 1_000_003
OFFSET = 987_654_321

# Multiplicative inverse for decoding
INVERSE_MULTIPLIER = pow(MULTIPLIER, -1, CAPACITY)


def scramble_id(number: int) -> int:
    """Scramble a database ID into a unique integer."""

    if not 0 <= number < CAPACITY:
        raise ValueError("ID is outside the supported range")

    return (number * MULTIPLIER + OFFSET) % CAPACITY


def unscramble_id(number: int) -> int:
    """Reverse the scrambling transformation."""

    if not 0 <= number < CAPACITY:
        raise ValueError("Scrambled ID is outside the supported range")

    return (
        (number - OFFSET) * INVERSE_MULTIPLIER
    ) % CAPACITY


def generate_short_code(link_id: int) -> str:
    """Generate a scrambled seven-character Base62 code."""

    return encode_base62(scramble_id(link_id))


def decode_short_code(code: str) -> int:
    """Recover the original ID from a scrambled code."""

    return unscramble_id(decode_base62(code))

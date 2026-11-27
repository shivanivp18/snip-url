
import pytest
from app.utils.base62 import generate_short_code, decode_short_code

from app.utils.base62 import (
    encode_base62,
    decode_base62,
)


@pytest.mark.parametrize(
    "number",
    [0, 1, 61, 62, 125, 99999, (62**7) - 1],
)
def test_base62_round_trip(number):
    code = encode_base62(number)

    assert len(code) == 7
    assert decode_base62(code) == number


def test_negative_number():
    with pytest.raises(ValueError):
        encode_base62(-1)


def test_number_too_large():
    with pytest.raises(ValueError):
        encode_base62(62**7)


def test_invalid_character():
    with pytest.raises(ValueError):
        decode_base62("00000!!")


def test_invalid_length():
    with pytest.raises(ValueError):
        decode_base62("abc")


def test_scrambled_code_round_trip():
    for link_id in [0, 1, 2, 125, 999999, (62**7) - 1]:
        code = generate_short_code(link_id)

        assert len(code) == 7
        assert decode_short_code(code) == link_id


def test_sequential_ids_have_unique_codes():
    codes = [generate_short_code(i) for i in range(1000)]

    assert len(codes) == len(set(codes))


def test_scrambled_codes_are_not_plain_ids():
    assert generate_short_code(1) != "0000001"
    assert generate_short_code(2) != "0000002"


def test_invalid_link_id():
    import pytest

    with pytest.raises(ValueError):
        generate_short_code(-1)

    with pytest.raises(ValueError):
        generate_short_code(62**7)

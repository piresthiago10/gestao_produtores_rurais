import pytest
from app.utils.cnpj_validator import validate_cnpj


@pytest.mark.parametrize(
    "cnpj, expected",
    [
        ("12.345.678/0001-95", True),
        ("12345678000195", True),
        ("", False),
        ("abc.def.ghi/jkl-mn", False),
        ("00.000.000/0000-00", False),
        ("12.345.678/0001", False),
        ("27865757000148", False),
    ],
)
def test_validate_cnpj(cnpj, expected):
    """Test the CNPJ validation function with various inputs."""
    assert validate_cnpj(cnpj) == expected

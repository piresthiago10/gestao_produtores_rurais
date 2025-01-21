import pytest
from app.utils.cpf_validator import validate_cpf


@pytest.mark.parametrize(
    "cpf, expected",
    [
        ("123.456.789-09", True),
        ("123.456.789-08", False),
        ("000.000.000-00", False),
        ("12345678909", True),
        ("", False),
        ("123.456.789", False),
        ("abc.def.ghi-jk", False),
        ("987.654.321-00", True),
        ("95867364517", False),
    ],
)
def test_validate_cpf(cpf, expected):
    """Testa a validação do CPF."""
    assert validate_cpf(cpf) == expected

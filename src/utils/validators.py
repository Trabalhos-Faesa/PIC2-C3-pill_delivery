from django.core.exceptions import ValidationError


def validate_digits(digits: str) -> None:
    if not digits.isdecimal():
        raise ValidationError(
            '"%(digits)s" deve ser composto apenas de dígitos',
            params={'digits': digits},
            code='digits-invalid'
        )


def validate_cpf(cpf: str) -> None:
    cpf_digits = [int(digit) for digit in cpf if digit.isdecimal()]

    if len(cpf_digits) != 11:
        raise ValidationError(
            'CPF "%(cpf)s" inválido pois não contém 11 caracteres numéricos',
            params={'cpf': cpf},
            code='cpf-invalid'
        )

    # # Verifica a formatação do CPF
    # if not re.match(r'\d{3}\.\d{3}\.\d{3}-\d{2}', cpf):
    #     return False
    if len(cpf_digits) != len(cpf):
        raise ValidationError(
            'CPF "%(cpf)s" inválido pois contém caracteres não numéricos',
            params={'cpf': cpf},
            code='cpf-invalid'
        )

    # Validação do primeiro dígito verificador:
    sum_of_products = sum(a*b for a, b in zip(cpf_digits[0:9], range(10, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    if cpf_digits[9] != expected_digit:
        raise ValidationError(
            'O primeiro dígito verificador do CPF "%(cpf)s" é inválido',
            params={'cpf': cpf},
            code='cpf-invalid'
        )

    # Validação do segundo dígito verificador:
    sum_of_products = sum(a*b for a, b in zip(cpf_digits[0:10], range(11, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    if cpf_digits[10] != expected_digit:
        raise ValidationError(
            'O segundo dígito verificador do CPF "%(cpf)s" é inválido',
            params={'cpf': cpf},
            code='cpf-invalid'
        )

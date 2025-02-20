def validate_cpf(cpf):  # noqa: C901
    """Valida se o CPF é válido."""
    cpf = cpf.replace(".", "").replace("-", "")

    if cpf == "00000000000":
        return False

    if len(cpf) == 11:
        validar = True
        digitos_verificadores = cpf[9:]
    else:
        return False

    cpf = cpf[:9]

    try:
        dig_1 = int(cpf[0]) * 1
        dig_2 = int(cpf[1]) * 2
        dig_3 = int(cpf[2]) * 3
        dig_4 = int(cpf[3]) * 4
        dig_5 = int(cpf[4]) * 5
        dig_6 = int(cpf[5]) * 6
        dig_7 = int(cpf[6]) * 7
        dig_8 = int(cpf[7]) * 8
        dig_9 = int(cpf[8]) * 9
    except Exception:
        return False

    dig_1_ao_9_somados = (
        dig_1 + dig_2 + dig_3 + dig_4 + dig_5 + dig_6 + dig_7 + dig_8 + dig_9
    )

    dig_10 = dig_1_ao_9_somados % 11

    if dig_10 > 9:
        dig_10 = 0

    cpf += str(dig_10)

    dig_1 = int(cpf[0]) * 0
    dig_2 = int(cpf[1]) * 1
    dig_3 = int(cpf[2]) * 2
    dig_4 = int(cpf[3]) * 3
    dig_5 = int(cpf[4]) * 4
    dig_6 = int(cpf[5]) * 5
    dig_7 = int(cpf[6]) * 6
    dig_8 = int(cpf[7]) * 7
    dig_9 = int(cpf[8]) * 8
    dig_10 = int(cpf[9]) * 9

    dig_1_ao_10_somados = (
        dig_1 + dig_2 + dig_3 + dig_4 + dig_5 + dig_6 + dig_7 + dig_8 + dig_9 + dig_10
    )

    dig_11 = dig_1_ao_10_somados % 11

    if dig_11 > 9:
        dig_11 = 0

    cpf_validado = cpf + str(dig_11)

    cpf = (
        cpf_validado[:3]
        + "."
        + cpf_validado[3:6]
        + "."
        + cpf_validado[6:9]
        + "-"
        + cpf_validado[9:]
    )

    if validar:
        if digitos_verificadores != cpf_validado[9:]:
            return False

    return True

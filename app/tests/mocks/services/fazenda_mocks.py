DASHBOARD_DATA = {
    "farms_by_culture": [
        {"tipo_cultura": "Milho", "total_farms": 1},
        {"tipo_cultura": "Soja", "total_farms": 1},
        {"tipo_cultura": "Trigo", "total_farms": 1},
    ],
    "farms_by_soil_use": [
        {"area_agricultavel": 300, "area_vegetacao": 200, "total_farms": 1},
        {"area_agricultavel": 500, "area_vegetacao": 250, "total_farms": 1},
        {"area_agricultavel": 700, "area_vegetacao": 300, "total_farms": 1},
    ],
    "farms_by_state": [
        {"state": "MG", "total_farms": 1},
        {"state": "SP", "total_farms": 2},
    ],
    "total_area": 2250,
    "total_farms": 3,
}

RESULT_FARM_WITH_CROPS = {
    "id": 1,
    "nome": "Fazenda Primavera",
    "cidade": "Ribeirão Preto",
    "estado": "SP",
    "area_total": 500,
    "area_agricultavel": 300,
    "area_vegetacao": 200,
    "ativo": True,
    "safras": [
        {
            "id": 1,
            "nome": "Safra de Soja 2023",
            "variedade": "Orgânico",
            "tipo_cultura": "Soja",
            "ano_colheita": 2024,
            "produtividade_tonelada": 50.5,
            "ativo": True,
        }
    ],
}

RESULT_FARM_WITHOUT_CROPS = {
    "id": 1,
    "nome": "Fazenda Primavera",
    "cidade": "Ribeirão Preto",
    "estado": "SP",
    "area_total": 500,
    "area_agricultavel": 300,
    "area_vegetacao": 200,
    "ativo": True,
    "safras": [],
}

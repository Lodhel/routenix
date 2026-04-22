record_list_responses = {
    200: {
        "description": "Успешный запрос",
        "content": {
            "application/json": {
                "examples": {
                    "success_example": {
                        "summary": "Список записей",
                        "value": {
                            "data": [
                                {
                                    "id": 1,
                                    "label": "Элемент A"
                                },
                                {
                                    "id": 2,
                                    "label": "Элемент B"
                                }
                            ],
                            "success": True
                        }
                    }
                }
            }
        }
    },
    401: {
        "description": "Ошибка авторизации",
        "content": {
            "application/json": {
                "examples": {
                    "unauthorized": {
                        "summary": "Токен не передан или невалиден",
                        "value": {
                            "error": "Ошибка аутентификации"
                        }
                    }
                }
            }
        }
    },
}

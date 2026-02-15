from drf_spectacular.utils import OpenApiExample, extend_schema

# ===== LOGIN SCHEMAS =====
email_login_schema = extend_schema(
    summary="Вход по email и паролю",
    description="Получить access и refresh токены используя email и пароль",
    tags=["Auth"],
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "email": {"type": "string", "format": "email"},
                "password": {"type": "string"},
            },
            "required": ["email", "password"],
            "example": {"email": "user@example.com", "password": "password123"},
        }
    },
    responses={
        200: {
            "type": "object",
            "properties": {"access": {"type": "string"}, "refresh": {"type": "string"}},
        },
        401: {"type": "object", "example": {"detail": "Invalid credentials"}},
    },
)

username_login_schema = extend_schema(
    summary="Вход по username и паролю",
    description="Получить access и refresh токены используя username и пароль",
    tags=["Auth"],
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "username": {"type": "string"},
                "password": {"type": "string"},
            },
            "required": ["username", "password"],
            "example": {"username": "john_doe", "password": "password123"},
        }
    },
    responses={
        200: {
            "type": "object",
            "properties": {"access": {"type": "string"}, "refresh": {"type": "string"}},
        },
        401: {"type": "object", "example": {"detail": "Invalid credentials"}},
    },
)

# ===== REFRESH TOKEN =====
refresh_token_schema = extend_schema(
    summary="Обновить access токен",
    description="Получить новый access токен используя refresh токен",
    tags=["Auth"],
)

# ===== LOGOUT =====
logout_schema = extend_schema(
    summary="Логаут",
    description="Инвалидировать refresh токен (добавить в blacklist)",
    tags=["Auth"],
    request={
        "application/json": {
            "type": "object",
            "properties": {"refresh": {"type": "string"}},
            "required": ["refresh"],
            "example": {"refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."},
        }
    },
    responses={
        200: {"type": "object", "example": {"detail": "Successfully logged out"}},
        400: {"type": "object", "example": {"detail": "Refresh token is required"}},
    },
)

# ===== CURRENT USER =====
current_user_schema = extend_schema(
    summary="Получить текущего пользователя",
    description="Получить информацию о текущем аутентифицированном пользователе",
    tags=["Auth"],
)

# ===== CHANGE PASSWORD =====
change_password_schema = extend_schema(
    summary="Изменить пароль",
    description="Изменить пароль текущего пользователя",
    tags=["Auth"],
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "old_password": {"type": "string"},
                "new_password": {"type": "string"},
                "new_password_confirm": {"type": "string"},
            },
            "required": ["old_password", "new_password", "new_password_confirm"],
            "example": {
                "old_password": "old_pass123",
                "new_password": "new_pass123",
                "new_password_confirm": "new_pass123",
            },
        }
    },
    responses={
        200: {"type": "object", "example": {"detail": "Password changed successfully"}},
        400: {"type": "object", "example": {"old_password": "Wrong password"}},
    },
)

# ===== VERIFY TOKEN =====
verify_token_schema = extend_schema(
    summary="Проверить валидность токена",
    description="Проверить, валиден ли access токен",
    tags=["Auth"],
    request={
        "application/json": {
            "type": "object",
            "properties": {"token": {"type": "string"}},
            "required": ["token"],
            "example": {"token": "eyJ0eXAiOiJKV1QiLCJhbGc..."},
        }
    },
    responses={
        200: {"type": "object", "example": {"valid": True}},
        400: {
            "type": "object",
            "example": {"valid": False, "detail": "Token is invalid or expired"},
        },
    },
)


# ===== SEND VERIFICATION CODE =====
send_verification_code_schema = extend_schema(
    summary="Отправить код верификации на email",
    description="Генерирует 6-значный код и отправляет его на указанный email",
    tags=["Auth"],
    request={
        "application/json": {
            "type": "object",
            "properties": {"email": {"type": "string", "format": "email"}},
            "required": ["email"],
            "example": {"email": "user@example.com"},
        }
    },
    responses={
        200: {
            "type": "object",
            "example": {"detail": "Код отправлен"},
        },
        400: {
            "type": "object",
            "example": {"email": "Обязательное поле"},
        },
    },
)

# ===== VERIFY CODE =====
verify_code_schema = extend_schema(
    summary="Подтвердить код верификации",
    description="Проверяет код, если верно — выдает temporary token для привязки или регистрации",
    tags=["Auth"],
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "email": {"type": "string", "format": "email"},
                "code": {"type": "string", "maxLength": 6},
            },
            "required": ["email", "code"],
            "example": {"email": "user@example.com", "code": "123456"},
        }
    },
    responses={
        200: {
            "type": "object",
            "example": {"temporary_token": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6"},
        },
        400: {
            "type": "object",
            "example": {"detail": "Неверный код"},
        },
    },
)

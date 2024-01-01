from fastapi import Request


class LoginForm:
    """
    Реализация проверки почты и пароля
    """
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: list = []
        self.username: str | None = None
        self.password: str | None = None

    async def load_data(self):
        form = await self.request.form()
        self.username = form.get(
            "email"
        )
        self.password = form.get("password")

    async def is_valid(self):
        if not self.username or not (self.username.__contains__("@")):
            self.errors.append("Требуется электронная почта")
        if not self.password or not len(self.password) >= 4:
            self.errors.append("Требуется действительный пароль")
        if not self.errors:
            return True
        return False


class UserCreateForm:
    """
    Реализация проверки почты, пароля и имени лля создания пользователя
    """
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: list = []
        self.username: str | None = None
        self.email: str | None = None
        self.password: str | None = None

    async def load_data(self):
        form = await self.request.form()
        self.username = form.get("username")
        self.email = form.get("email")
        self.password = form.get("password")

    async def is_valid(self):
        if not self.username or not len(self.username) > 3:
            self.errors.append("Имя пользователя должно быть > 3 символов.")
        if not self.email or not (self.email.__contains__("@")):
            self.errors.append("Требуется электронная почта")
        if not self.password or not len(self.password) >= 4:
            self.errors.append("Пароль должен содержать > 4 символов")
        if not self.errors:
            return True
        return False

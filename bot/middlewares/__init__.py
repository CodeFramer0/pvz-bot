from loader import dp

from .throttling import ThrottlingMiddleware
from .user_exists import UserExistsMiddleware

if __name__ == "middlewares":
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(UserExistsMiddleware())

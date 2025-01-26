from . import users, auth

routers = [
    auth.router,
    users.router,
]

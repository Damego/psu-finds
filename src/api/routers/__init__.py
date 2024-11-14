from . import users, items, auth

routers = [
    auth.router,
    users.router,
    items.router,
]

from django.urls import include, path
from rest_framework.routers import DynamicRoute, Route, SimpleRouter

from .views import IngredientItemViewSet, DishViewSet, RecipeTagViewSet, UsersViewSet
from users.urls import auth_urls

class UsersRouter(SimpleRouter):
    routes = [
        DynamicRoute(
            url=r'^{prefix}/{url_path}{trailing_slash}$',
            name='{basename}-{url_name}',
            detail=True,
            initkwargs={}
        ),
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                'get': 'list',
                'post': 'create'
            },
            name='{basename}-list',
            detail=False,
            initkwargs={'suffix': 'List'}
        ),
        Route(
            url=r'^{prefix}/{lookup}{trailing_slash}$',
            mapping={
                'get': 'retrieve',
                'patch': 'partial_update',
                'delete': 'destroy'
            },
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Instance'}
        ),
    ]


users_router = UsersRouter()
users_router.register('', UsersViewSet)


router = SimpleRouter()
router.register('ingredients', IngredientItemViewSet)
router.register('tags', RecipeTagViewSet)
router.register('recipes', DishViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('v1/users/', include(users_router.urls)),
    path('v1/auth/', include(auth_urls)),
]

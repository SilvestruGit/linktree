"""
URL mappings for the linktree app.
"""

from linktree.views import LinkTreeViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('linktrees', LinkTreeViewSet)

app_name = 'linktree'

urlpatterns = router.urls

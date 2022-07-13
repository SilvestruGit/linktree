"""
Views for the linktree API.
"""

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from linktree.serializer import LinkTreeSerializer
from core.models import LinkTree


class LinkTreeViewSet(viewsets.ModelViewSet):
    """Viewset for viewing and editing linktrees."""
    serializer_class = LinkTreeSerializer
    queryset = LinkTree.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Get linktrees for auth user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')

from rest_framework.permissions import BasePermission

class IsRecruiter(BasePermission):
    """
    Permission permettant uniquement aux recruteurs d'accéder à la vue.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'recuteur'

class IsCandidate(BasePermission):
    """
    Permission permettant uniquement aux candidats d'accéder à la vue.
    """
    def has_permission(self, request, view):
        # Vérifie si l'utilisateur est authentifié et est recruteur et admin ou propriétaire de l'offre
        return request.user.is_authenticated and request.user.user_type == 'recruteur' or request.user.is_staff
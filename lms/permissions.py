from rest_framework import permissions

class IsInstructorOrReadOnly(permissions.BasePermission):
    """
    Satpam RBAC:
    - Jika cuma mau lihat data (GET), biarkan masuk.
    - Jika mau nambah data (POST), cek dulu apakah dia Instruktur/Admin (is_staff).
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return bool(request.user and request.user.is_staff)
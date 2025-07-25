# from django.core.exceptions import PermissionDenied

# class RoleRequiredMixin:
#     allowed_user = [] #Set this in the View
#     def dispatch(self, request, *args, **kwargs):
#         user_role = getattr(request.user.profile, 'role', None)
#         if user_role not in self.allowed_user and not request.user.is_superuser:
#             raise PermissionDenied("ທ່ານບໍ່ມີສິດໃນການເຂົ້າເຖິງຫນ້ານີ້")
#         return super().dispatch(request, *args, **kwargs)
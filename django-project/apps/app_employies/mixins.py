# from django.core.exceptions import PermissionDenied


# class EmployeeOwnerRequestMixin:
#     model_user_field = "user"
#     def dispatch(self, request, *args, **kwargs):
#         obj = self.get_object()
#         if obj.user != request.user and not request.user.is_superuser:
#             raise PermissionDenied("ທ່ານບໍ່ມີສິດເຂົ້າເຖິງຂໍ້ມູນນີ້")
#         return super().dispatch(request, *args, **kwargs)
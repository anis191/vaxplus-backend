from rest_framework.pagination import PageNumberPagination

class PatientsPagination(PageNumberPagination):
    page_size = 10

# class DoctorsPagination(PageNumberPagination):
    # page_size = 15

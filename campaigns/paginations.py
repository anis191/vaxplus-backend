from rest_framework.pagination import PageNumberPagination

class DefaultPagination(PageNumberPagination):
    page_size = 5

class VaccinationRecordPagination(PageNumberPagination):
    page_size = 15

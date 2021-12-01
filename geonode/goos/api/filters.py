from rest_framework.filters import BaseFilterBackend
import logging

logger = logging.getLogger(__name__)


class EovFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if request.query_params.get("eovs"):
            eov_ids = [eid for eid in request.query_params.get("eovs").split(",")]
            queryset = queryset.filter(eovs__in=eov_ids).distinct()
        return queryset

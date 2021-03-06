import logging

from django.conf.urls.defaults import *
from clothes.models import *

from django.conf.urls.defaults import url, patterns, include
from rest_framework import viewsets, routers
from .serializers import DateSerializer

# ViewSets define the view behavior.


class ColorViewSet(viewsets.ReadOnlyModelViewSet):
    model = Color


class StoreViewSet(viewsets.ReadOnlyModelViewSet):
    model = Store


class ArticleTypeViewSet(viewsets.ReadOnlyModelViewSet):
    model = ArticleType


class ArticleViewSet(viewsets.ReadOnlyModelViewSet):
    model = Article
    paginate_by = 10


class AccessorizedOutfitViewSet(viewsets.ReadOnlyModelViewSet):
    model = AccessorizedOutfit
    paginate_by = 10

class DateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Date.objects.extra(order_by=['-date'])
    paginate_by = 10
    paginate_by_param = 'page_size'
    serializer_class = DateSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned dates to a year and month.
        """
        queryset = Date.objects.all()

        yearmonth = self.request.QUERY_PARAMS.get('yearmonth', None)
        if yearmonth is not None:
            year = int(yearmonth[:4])
            month = int(yearmonth[4:])
            logging.info('Filtering dates to %s, %s', year, month)
            queryset = (queryset
                .filter(date__year=year)
                .filter(date__month=month))

        return queryset


# Routers provide an easy way of automatically determining the URL conf
router = routers.DefaultRouter()
router.register(r'colors', ColorViewSet)
router.register(r'stores', StoreViewSet)
router.register(r'articletypes', ArticleTypeViewSet)
router.register(r'articles', ArticleViewSet)
router.register(r'dates', DateViewSet)
router.register(r'accessorizedoutfits', AccessorizedOutfitViewSet)

urlpatterns = patterns(
    'clothes_data.views',
    url(r'^', include(router.urls)),
)

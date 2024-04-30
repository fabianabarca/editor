from django.contrib import admin
from .models import *

admin.site.register(Provider)
admin.site.register(Feed)
admin.site.register(Agency)
admin.site.register(Calendar)
admin.site.register(CalendarDate)
admin.site.register(Route)
admin.site.register(Stop)
admin.site.register(StopTime)
admin.site.register(Trip)
admin.site.register(Shape)
admin.site.register(GeoShape)
admin.site.register(FareAttribute)
admin.site.register(FareRule)
admin.site.register(FeedInfo)

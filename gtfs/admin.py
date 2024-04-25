from django.contrib import admin
from .models import Agency, CalendarDate, Route, FareAttribute, Feed, Company, Zone, FeedInfo, Stop

admin.site.register(Agency)
admin.site.register(CalendarDate)
admin.site.register(Route)
admin.site.register(FareAttribute)
admin.site.register(Feed)
admin.site.register(Company)
admin.site.register(Zone)
admin.site.register(FeedInfo)
admin.site.register(Stop)


from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.utils.translation import ugettext_lazy

# Text to put at the end of each page's <title>.
admin.site.site_title = ugettext_lazy('{} admin site'.format(settings.APP_NAME))

# Text to put in each page's <h1> (and above login form).
admin.site.site_header = ugettext_lazy('{} administration'.format(settings.APP_NAME))

# Text to put at the top of the admin index page.
admin.site.index_title = ugettext_lazy('Site administration')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('boards.urls')),
]

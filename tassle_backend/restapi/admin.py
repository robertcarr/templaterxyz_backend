from django.contrib import admin

from .models import Repos, Templates, UserProfile, User, Stats

admin.site.register(Repos)
admin.site.register(Templates)
admin.site.register(UserProfile)
admin.site.register(User)
admin.site.register(Stats)


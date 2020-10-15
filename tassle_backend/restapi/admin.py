from django.contrib import admin

from .models import Repos, Templates, UserProfile, User

admin.site.register(Repos)
admin.site.register(Templates)
admin.site.register(UserProfile)
admin.site.register(User)


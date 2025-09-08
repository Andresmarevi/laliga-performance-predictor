from django.contrib import admin
from .models import GoalkeeperMatch, DefenderMatch, MidfielderMatch, ForwardMatch

admin.site.register(GoalkeeperMatch)
admin.site.register(DefenderMatch)
admin.site.register(MidfielderMatch)
admin.site.register(ForwardMatch)

from django.contrib import admin

from .models import Agent, Shift, AgentShift, Residence, Category


admin.site.register(Agent)
admin.site.register(Shift)
admin.site.register(AgentShift)
admin.site.register(Residence)
admin.site.register(Category)

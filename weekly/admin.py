from django.contrib import admin

from .models import Agent, Shift, AgentShift, Residence, Category, Document


admin.site.register(Agent)
admin.site.register(Shift)
admin.site.register(AgentShift)
admin.site.register(Residence)
admin.site.register(Category)
admin.site.register(Document)

# Admin panel
title = "Gestión de turnos y agentes"
subtitle = "Panel de gestión"

admin.site.site_header = title
admin.site.site_title = title
admin.site.index_title = subtitle

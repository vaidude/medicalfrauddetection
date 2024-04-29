from django.contrib import admin
from  .models  import reg,adminreg,agent,Patient,Providers,PredictionResult
# Register your models here.

admin.site.register(reg)
admin.site.register(adminreg)
admin.site.register(agent)
admin.site.register(Patient)
admin.site.register(Providers)

admin.site.register(PredictionResult)

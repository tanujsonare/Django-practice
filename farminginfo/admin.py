from django.contrib import admin
from farminginfo.models import crops_info
from farminginfo.models import account_info
from farminginfo.models import crop_detail
from import_export.admin import ImportExportModelAdmin

class farming_admin(ImportExportModelAdmin):
    pass


admin.site.register(account_info)
admin.site.register(crops_info)
admin.site.register(crop_detail,farming_admin)
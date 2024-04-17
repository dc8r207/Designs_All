from django.contrib import admin

from .models import work_type,designer,progress_mile_stone,filed_office,bwdb_project,design_work
from .models import design_work_progress
from import_export.admin import ImportExportModelAdmin
from import_export import resources

#registering work_type
class work_type_resource(resources.ModelResource):
    class Meta:
        model=work_type
class work_type_admin(ImportExportModelAdmin):
    resource_classes=[work_type_resource]
admin.site.register(work_type,work_type_admin)

#registering designer

class designer_resource(resources.ModelResource):
    class Meta:
        model=designer
class designer_admin(ImportExportModelAdmin):
    resource_classes=[designer_resource]
admin.site.register(designer,designer_admin)




#registering progress_mile_stone

class progress_mile_stone_resource(resources.ModelResource):
    class Meta:
        model=progress_mile_stone
class progress_mile_stone_admin(ImportExportModelAdmin):
    resource_classes=[progress_mile_stone_resource]

admin.site.register(progress_mile_stone,progress_mile_stone_admin)

#registering filed_office
class filed_office_resource(resources.ModelResource):
    class Meta:
        model=filed_office
        
class filed_office_admin(ImportExportModelAdmin):
    resource_classes=[filed_office_resource]
    
admin.site.register(filed_office,filed_office_admin)



#registering proect
class bwdb_project_resource(resources.ModelResource):
    class Meta:
        model=bwdb_project
        
class bwdb_project_admin(ImportExportModelAdmin):
    resource_classes=[bwdb_project_resource]
    
admin.site.register(bwdb_project,bwdb_project_admin)

#registering work_name
class design_work_resource(resources.ModelResource):
    class Meta:
        model=design_work
        
class design_work_admin(ImportExportModelAdmin):
    resource_classes=[design_work_resource]
    
admin.site.register(design_work,design_work_admin)

#registering design_work_progress
class design_work_progress_resource(resources.ModelResource):
    class Meta:
        model=design_work_progress
        
class design_work_progress_admin(ImportExportModelAdmin):
    resource_classes=[design_work_progress_resource]
    
admin.site.register(design_work_progress,design_work_progress_admin)

from .models import design_work_completion_status
#registering design_work_completion_status
class design_work_completion_status_resource(resources.ModelResource):
    class Meta:
        model=design_work_completion_status
        
class  design_work_completion_status_admin(ImportExportModelAdmin):
    resource_classes=[design_work_completion_status_resource]
    
admin.site.register(design_work_completion_status,design_work_completion_status_admin)





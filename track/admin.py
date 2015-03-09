from django.contrib import admin
from track.models import Bug,User,Version,Project,Modules,Team
from bugTrack.jpush import jpushMobile

# Register your models here.

class bugAdmin(admin.ModelAdmin):
    list_display = ('name', 'content', 'version','project','date','state','distribter','urgency','platform','pic')
    list_filter = ('date',)
    search_fields = ('name','version','date')
    date_hierarchy = 'date'
    ordering = ('-date','-version','-urgency')
    def save_model(self, request, obj, form, change):
        if form and obj.push == True:
            jpushMobile.jpushios(obj)
        obj.save()

class UserAdmin(admin.ModelAdmin):
    list_display = ('username','email','team')

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project','version')

admin.site.register(Bug,bugAdmin)
admin.site.register(User,UserAdmin)
admin.site.register(Project,ProjectAdmin)
admin.site.register(Version)
admin.site.register(Modules)
admin.site.register(Team)
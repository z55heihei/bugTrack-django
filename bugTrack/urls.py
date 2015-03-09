from django.conf.urls import include, url,patterns
from django.contrib import admin
from bugTrack.views import bugView,userView,moduleView,teamView,projectView,versionView
from bugTrack import view
from track.routers import *


urlpatterns = patterns('',
    url(r'^admin',include(admin.site.urls)),
    url(r'^getMybugs/$', bugView.getMyBugs),
    url(r'^bugSend/$',bugView.bugSend),
    url(r'^delBug/$',bugView.delBug),
    url(r'^modifyBug/$',bugView.modifyBug),
    url(r'^modifyUser/$',userView.modifyUser),
    url(r'^allUser/$',userView.allUser),
    url(r'delUser/$',userView.delUser),
    url(r'^register/$',userView.register),
    url(r'^login/$',userView.login),
    url(r'^creatModule/$',moduleView.creatModule),
    url(r'^getModules/$',moduleView.getModules),
    url(r'^delModule/$',moduleView.delModule),
    url(r'^creatTeam/$',teamView.creatTeam),
    url(r'^getTeams/$',teamView.getTeams),
    url(r'^delTeam/$',teamView.delTeam),
    url(r'^getProjects/$',projectView.getProjects),
    url(r'^creatProject/$',projectView.creatProject),
    url(r'^delProject/$',projectView.delProject),
    url(r'^getVersions/$',versionView.getVersions),
    url(r'^delVersion/$',versionView.delVersion),
    url(r'^creatVersion',versionView.creatVersion),
    url(r'^paramsTest/$',view.paramsTest),
)

urlpatterns += patterns('',
    url(r'^',include(router.urls)),
    url(r'^api-auth/',include('rest_framework.urls',namespace='rest_framework'))
)


'''
urlpatterns += patterns( '',
    url( r'^grappelli/', include( 'grappelli.urls' ) ),
)
'''
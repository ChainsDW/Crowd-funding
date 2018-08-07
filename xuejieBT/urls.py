"""xuejieBT URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include
from jiuchai import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'wotou/crowdfunding/index.html', views.index),
    # path('wotou/crowdfunding/blockchians.html', views.view_traslations),
    url(r'mine', views.mine),
    url(r'transactions/new', views.create_transaction),
    url(r'wotou/crowdfunding/chain', views.view_chain),
    url(r'^chain/transactions$', views.view_trans),
    url(r'nodes/register', views.register_nodes),
    url(r'nodes/resolve', views.consensus),
    #url(r'wotou/crowdfunding/new', views.new_crowdfund),
    #我自己加的一部分
    url('index',views.index),
    url('post_data',views.post_data),
    url('jiucai',views.index_jiucai),
    url('homepage',views.homepage),
    url('^download.html$', views.download),
    # url('download_chain.html', views.download_chain),
    url('^each/trans.html$', views.project_trans),
    url('^login.html$', views.acc_login),
    url('^register.html$', views.register),
    url('send_msg/', views.send_msg),
    url('^myCrowdfunding$', views.myCrowdfunding),
    url('^myCrowdfunding/getData$', views.get_user_data),
    # 审核人员页面
    url(r'^audit/', include('Audit.urls')),
]

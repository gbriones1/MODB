from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
	url(r'reports/differences/products/$', 'database.views.product_diff', name='product_diff'),
	url(r'reports/differences/providers/$', 'database.views.provider_diff', name='provider_diff'),
	url(r'reports/differences/storage/$', 'database.views.storage_diff', name='storage_diff'),
	url(r'reports/shopping/$', 'database.views.shopping', name='shopping'),
	url(r'reports/expenses/$', 'database.views.expenses', name='expenses'),
	url(r'reports/$', 'database.views.reports', name='reports'),
	url(r'product/(?P<id>\w+\W*\w*)/$', 'database.views.product', name='product'),
	url(r'tool/(?P<id>\w+\W*\w*)/$', 'database.views.tool', name='tool'),
	url(r'tools/$', 'database.views.tools', name='tools'),
	url(r'inputs/$', 'database.views.inputs', name='inputs'),
	url(r'outputs/$', 'database.views.outputs', name='outputs'),
	url(r'lendings/$', 'database.views.lendings', name='lendings'),
	url(r'providers/$', 'database.views.providers', name='providers'),
	url(r'brands/$', 'database.views.brands', name='brands'),
	url(r'appliances/$', 'database.views.appliances', name='appliances'),
	url(r'classifications/$', 'database.views.classifications', name='classifications'),
	url(r'registry/$', 'database.views.registry', name='registry'),
	url(r'settings/$', 'database.views.settings', name='settings'),
	url(r'^$', 'database.views.dashboard', name='dashboard'),
)
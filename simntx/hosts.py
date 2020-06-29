from django_hosts import patterns, host

host_patterns = patterns('',
    host('', 'simntx.urls', name = 'simntx'),
    host('vendor', 'vendor.urls', name = 'vendor'),
)
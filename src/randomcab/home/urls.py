"""
    urls.py
    Copyright 2015 Jeroen Arnoldus <jeroen@repleo.nl>
    
THIS SOFTWARE IS SUPPLIED WITHOUT WARRANTY OF ANY KIND, AND MAY BE
COPIED, MODIFIED OR DISTRIBUTED IN ANY WAY, AS LONG AS THIS NOTICE
AND ACKNOWLEDGEMENT OF AUTHORSHIP REMAIN.

2015-01-10
  - urls resolver
"""

__author__ = "Jeroen Arnoldus <jeroen@repleo.nl>"
__version__ = "$Rev$"
__date__ = "$Date$"
__copyright__ = "Copyright: 2015 Jeroen Arnoldus;"
from django.conf.urls import patterns, url
from randomcab.home.views import IndexView
from randomcab.home.views import SuccessView

urlpatterns = patterns('',
     url(r'^$', IndexView.as_view(), name='randomcab-home-index'),
     url(r'^success', SuccessView.as_view(), name='randomcab-home-success'),
)
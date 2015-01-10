"""
    view.py
    Copyright 2015 Jeroen Arnoldus <jeroen@repleo.nl>
    
THIS SOFTWARE IS SUPPLIED WITHOUT WARRANTY OF ANY KIND, AND MAY BE
COPIED, MODIFIED OR DISTRIBUTED IN ANY WAY, AS LONG AS THIS NOTICE
AND ACKNOWLEDGEMENT OF AUTHORSHIP REMAIN.

2015-01-10
  -Core application of randomcab. Implements the formview for sending a 
  message. When it sends a message, flicker will be queried for an random
  picture which is attached to the email
  
USAGE:
 - define FLICKR_API_KEY and FLICKR_API_SECRET in settings.pyt
 
EXTERNAL DEPENCIES
 - Python3 requests
 - Python3 widgets
"""

__author__ = "Jeroen Arnoldus <jeroen@repleo.nl>"
__version__ = "$Rev$"
__date__ = "$Date$"
__copyright__ = "Copyright: 2015 Jeroen Arnoldus;"

import random
import requests
from email.mime.image import MIMEImage

from django.views.generic.edit import FormView
from django.views.generic import TemplateView;
from django.core.urlresolvers import reverse_lazy
from django.template import loader
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django import forms

from randomcab.home import flickr
from django.conf import settings

import logging
logger = logging.getLogger(__name__)

FLICKR_API_KEY = getattr(settings, 'FLICKR_API_KEY', "")
if not FLICKR_API_KEY:
        raise Exception("Please provide a valid FLICKR_API_KEY in settings file");
FLICKR_API_SECRET = getattr(settings, 'FLICKR_API_SECRET', "")
if not FLICKR_API_SECRET:
        raise Exception("Please provide a valid FLICKR_API_SECRET in settings file");
    
class MailForm(forms.Form):
    subject = forms.CharField(required=False)
    message = forms.CharField(widget=forms.Textarea,required=False)
    email_from = forms.EmailField(required=True)
    email_to = forms.EmailField(required=True)
    
    email_template_name = 'randomcab/home/mail/email.txt'
    html_email_template_name = 'randomcab/home/mail/email.html'
    

    def obtainRandomTaxiPicture(self):
        page=random.randint(1,50)
        flickr.API_KEY = FLICKR_API_KEY
        flickr.API_SECRET = FLICKR_API_SECRET
        taxis=flickr.photos_search(page=str(page),\
                                  tags="taxi",\
                                  text="taxi",\
                                  sort="interestingness-desc",\
                                  safe_search="3",\
                                  content_type="1",\
                                  in_gallery="true")
        i = 100
        while i > 0:
            i = i - 1
            taxi=taxis[random.randint(1,len(taxis))]
            logger.info("Obtain picture: %s" % taxi.getLarge())
            r=requests.get(taxi.getLarge())
            #Check if picture is available, if it is not available flickr will return a png
            if r.headers['content-type']=="image/jpeg":
                return r.content
        raise Exception("Could not obtain taxi picture URL")
            
    def sendmail(self):
        message = self.cleaned_data.get('message')
        subject = self.cleaned_data.get('subject')
        email_from = self.cleaned_data.get('email_from')
        email_to = self.cleaned_data.get('email_to')
        c = {
            'message':message,
            'subject':subject
        }
        email = strip_tags(loader.render_to_string(self.email_template_name, c))

        if self.html_email_template_name:
            html_email = loader.render_to_string(self.html_email_template_name, c)
        else:
            html_email = None
        
        log_email=getattr(settings, 'LOG_EMAIL', "")
        mail = EmailMultiAlternatives(subject, email, email_from,
            [email_to], [log_email,email_from])
        mail.attach_alternative(html_email, "text/html")
        
        taxi_img =self.obtainRandomTaxiPicture()
        taxi_img_mime=MIMEImage(taxi_img)
        taxi_img_mime.add_header('Content-Id', '<taxi.jpg>')  
        taxi_img_mime.add_header("Content-Disposition", "inline", filename="taxi.jpg")
        mail.mixed_subtype = 'related'
        mail.attach(taxi_img_mime)

        mail.send(); 
        
        
        
class IndexView(FormView):
    template_name = "randomcab/home/index.html"
    form_class = MailForm
    success_url = reverse_lazy('randomcab-home-success')


    def form_valid(self, form):
        form.sendmail();
        return super().form_valid(form)

    def get_context_data(self, **kwargs):        
        kwargs['success']=False
        context = super().get_context_data(**kwargs);
        return context

    
class SuccessView(TemplateView):
    template_name = "randomcab/home/index.html"

    def get_context_data(self, **kwargs):        
        kwargs['success']=True
        context = super().get_context_data(**kwargs);
        return context

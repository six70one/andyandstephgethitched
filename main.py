#!/usr/bin/env python
#
#http://dojotoolkit.org/reference-guide/quickstart/


import datetime
import os
#os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from google.appengine.dist import use_library
use_library('django', '1.2')

from datetime import date
from datetime import timedelta
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
from google.appengine.ext import db

def isIE(self):
    ua=self.request.headers.get("User-Agent")
    if "MSIE" in ua:
        return True
    else:
        return False

class ImportantDates(db.Model):
  name = db.StringProperty(multiline=False)
  date = db.DateProperty()

#weddingdate = datetime.date(2011,12,1)

def writeJQuery(self):
    self.response.out.write("""<script type="text/javascript" src="js/jquery-1.5.2.min.js"></script>
<script type="text/javascript" src="js/jquery.blockUI.js"></script>
<script type="text/javascript" src="js/slides.min.jquery.js"></script>
""")

def writeSlidePlayerScript(self):
    self.response.out.write("""
<script type="text/javascript">  
    $(function()
    {
        $("#slides").slides(
        {
            preload: true,
            preloadImage: 'img/loading.gif',
            play: 5000,
            pause: 2500,
            hoverPause: true
        });
    });
</script>""")

def writeJavascript(self):
    try:
        weddingdate = db.GqlQuery("SELECT * FROM ImportantDates where name='weddingday'")
        d = weddingdate.get().date.strftime("%A %m/%d/%Y")
    except AttributeError:
        a=ImportantDates()
        a.name='weddingday'
        a.date=datetime.date(2011,10,28)
        a.put()
        weddingdate = db.GqlQuery("SELECT * FROM ImportantDates where name='weddingday'")
        d = weddingdate.get().date.strftime("%A %m/%d/%Y")

    self.response.out.write("""<script type="text/javascript">
        $(document).ready(function() 
        {
            $("#why:hidden:first").fadeIn(6000);
        });
        </script>""")
    self.response.out.write("""<script type="text/javascript">        
        $(function() 
        {
            $('#wrapper').click(function()
            {
                $('#answer').replaceWith("<div id=date>because the wedding's not 'til %s!!!</div>");
                $('#why').replaceWith("<div id=why>need more <strong><a href=/details>details</a>???</strong></div><p>");
            });
        });
        
        </script>"""  % (d))
    



def writeDoctype(self):
#    self.response.out.write("""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\r\n""")
    self.response.out.write("""<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">\r\n""")

def writeMeta(self):
  self.response.out.write("""<meta http-equiv="content-type" content="text/html; charset=UTF-8"/>\r\n<meta http-equiv="cache-control" content="no-cache"/>\r\n""")

def writeHeader(self):
  writeDoctype(self)
  self.response.out.write("""<head>\r\n""");
  writeMeta(self)
  writeJQuery(self)
  writeJavascript(self)
  self.response.out.write("""<link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />""")
  self.response.out.write("""<title>Seriously, are they married yet?</title>\r\n""")
  self.response.out.write("""</head>\r\n\r\n""");
  self.response.out.write("""<body><div id=wrapper><div id=innerwrapper>\r\n""")

def writeTracker(self):
  self.response.out.write("""
  <script type="text/javascript">

  var _gaq = _gaq || [];
  _gaq.push(['_setAccount', 'UA-21684627-1']);
  _gaq.push(['_setDomainName', 'none']);
  _gaq.push(['_setAllowLinker', true]);
  _gaq.push(['_trackPageview']);

  (function() {
    var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
    ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
  })();

</script>""")

def writeNav(self):
    weddingdate = db.GqlQuery("SELECT * FROM ImportantDates where name='weddingday'")
    nw = date.fromordinal((datetime.datetime.now()-timedelta(hours=7)).toordinal())
    
    dow = nw.strftime("%A")
    diff = weddingdate.get().date-nw
    
    if diff.days > 0:
        aremarried = False
        nDays = diff.days
    else:
        aremarried = True
        nDays = diff.days*-1
    
    template_values = {
        'dayoftheweek': dow,
        'days': nDays,
        'happened' : aremarried,
    }

    path = os.path.join(os.path.dirname(__file__), 'static/templates/nav.html')
    self.response.out.write(template.render(path, template_values))

class MainHandler(webapp.RequestHandler):
    def get(self):
        writeHeader(self)
        weddingdate = db.GqlQuery("SELECT * FROM ImportantDates where name='weddingday'")
        
        if weddingdate.get().date < datetime.date.today():
            self.response.out.write("""<div id=over>YUP!</div>""")
            self.response.out.write("""<div id=utxt><a href="/details">find out how it went</a>...""")
        else:
            self.response.out.write("<div id=answer>nope, not yet</div><p>")
            self.response.out.write("""<div id="why" style="display:none"><a href="#">find out why</a>...""")
        
        writeTracker(self)

        self.response.out.write("</body>")

class DetailsHandler(webapp.RequestHandler):
    def get(self):
        writeDoctype(self)
        self.response.out.write("""<head>\r\n""");
        writeMeta(self)
        writeJQuery(self)
        writeSlidePlayerScript(self)
        self.response.out.write("""<link type="text/css" rel="stylesheet" href="/stylesheets/nav.css" />""")
        self.response.out.write("""<link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />""")
        self.response.out.write("""<title>Seriously, are they married yet?</title>\r\n""")
        self.response.out.write("""</head>\r\n\r\n""");
        writeNav(self)
        template_values = {}
        
        path = os.path.join(os.path.dirname(__file__), 'static/templates/details.html')
        self.response.out.write(template.render(path, template_values))

## TODO: change the sm_frame and sm_framed_pic to be the same overall size so that they line up.  or just add the frame to the static image...

class WherewhenHandler(webapp.RequestHandler):
    def get(self):
        writeDoctype(self)
        self.response.out.write("""<head>\r\n""");
        writeMeta(self)
        writeJQuery(self)
        writeSlidePlayerScript(self)
        self.response.out.write("""<link type="text/css" rel="stylesheet" href="/stylesheets/nav.css" />""")
        self.response.out.write("""<link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />""")
        self.response.out.write("""<title>Seriously, are they married yet?</title>\r\n""")
        self.response.out.write("""</head>\r\n\r\n""");
        writeNav(self)
        template_values = {}
        
        path = os.path.join(os.path.dirname(__file__), 'static/templates/wherewhen.html')
        self.response.out.write(template.render(path, template_values))

class FunStuffHandler(webapp.RequestHandler):
    def get(self):
        writeDoctype(self)
        self.response.out.write("""<head>\r\n""");
        writeMeta(self)
        writeJQuery(self)
        writeSlidePlayerScript(self)
        self.response.out.write("""<link type="text/css" rel="stylesheet" href="/stylesheets/nav.css" />""")
        self.response.out.write("""<link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />""")
        self.response.out.write("""<title>Seriously, are they married yet?</title>\r\n""")
        self.response.out.write("""</head>\r\n\r\n""");
        writeNav(self)
        template_values = {}
        
        path = os.path.join(os.path.dirname(__file__), 'static/templates/funstuff.html')
        self.response.out.write(template.render(path, template_values))

class OtherStuffHandler(webapp.RequestHandler):
    def get(self):
        writeDoctype(self)
        self.response.out.write("""<head>\r\n""");
        writeMeta(self)
        writeJQuery(self)
        writeSlidePlayerScript(self)
        self.response.out.write("""<link type="text/css" rel="stylesheet" href="/stylesheets/nav.css" />""")
        self.response.out.write("""<link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />""")
        self.response.out.write("""<title>Seriously, are they married yet?</title>\r\n""")
        self.response.out.write("""</head>\r\n\r\n""");
        writeNav(self)
        template_values = {}
        
        path = os.path.join(os.path.dirname(__file__), 'static/templates/stuff.html')
        self.response.out.write(template.render(path, template_values))

class UserAgentHandler(webapp.RequestHandler):
    def get(self):
        ua=self.request.headers.get("User-Agent")
        if "MSIE" in ua:
            self.response.out.write("IE\n")
        else:
            self.response.out.write("not IE\n")
        self.response.out.write(ua)

class CreateHandler(webapp.RequestHandler):
    def get(self):
        a=ImportantDates()
        a.name='weddingday'
        a.date=datetime.date(2011,10,28)
        a.put()
        self.response.out.write("OK")
        
class RobotHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write("""User-agent: Baiduspider<br>""")
        self.response.out.write("""Disallow: /<br><br>""")
        self.response.out.write("""User-agent: *<br>""")
        self.response.out.write("""Disallow: """)

def main():
    application = webapp.WSGIApplication([('/', MainHandler),
                                          ('/details',DetailsHandler),
                                          ('/wherewhen',WherewhenHandler),
                                          ('/fun',FunStuffHandler),
                                          ('/stuff',OtherStuffHandler),
                                          ('/createstuff',CreateHandler),
                                          ('/useragent', UserAgentHandler),
                                          ('/robots.txt',RobotHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()

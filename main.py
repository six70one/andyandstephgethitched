#!/usr/bin/env python
#
import datetime
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

from google.appengine.ext import db

class ImportantDates(db.Model):
  name = db.StringProperty(multiline=False)
  date = db.DateProperty()

#weddingdate = datetime.date(2011,12,1)

def writeDoctype(self):
  self.response.out.write("""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\r\n""")

def writeMeta(self):
  self.response.out.write("""<meta http-equiv="content-type" content="text/xhtml; charset=utf-8"/>\r\n<meta http-equiv="cache-control" content="no-cache"/>\r\n""")

def writeHeader(self):
  writeDoctype(self)
  self.response.out.write("""<html xmlns="http://www.w3.org/1999/xhtml">\r\n""")
  self.response.out.write("""<head>\r\n""");
  writeMeta(self)
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

class MainHandler(webapp.RequestHandler):
    def get(self):
        #a  = ImportantDates()
        #a.name='weddingday'
        #a.date=datetime.date(2011,12,1)
        #a.put()
        writeHeader(self)
        weddingdate = db.GqlQuery("SELECT * FROM ImportantDates where name='weddingday'")
        
        if weddingdate.get().date < datetime.date.today():
            self.response.out.write("<div id=answer>YUP!</div>")
        else:
            self.response.out.write("<div id=answer>nope, not yet</div><p>")
            self.response.out.write("""<div id=why>find out <strong><a href="/details">why</a></strong></div><p>""")
        
        writeTracker(self)
        self.response.out.write("</body>")

class DetailsHandler(webapp.RequestHandler):
    def get(self):
        writeHeader(self)
        self.response.out.write("<div id=why>Because it's not time yet...</div>")
        self.response.out.write("</body>")
        
def main():
    application = webapp.WSGIApplication([('/', MainHandler),
                                          ('/details',DetailsHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()

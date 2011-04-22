#!/usr/bin/env python
#
#http://dojotoolkit.org/reference-guide/quickstart/


import datetime
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

from google.appengine.ext import db

class ImportantDates(db.Model):
  name = db.StringProperty(multiline=False)
  date = db.DateProperty()

#weddingdate = datetime.date(2011,12,1)

def writeJQuery(self):
    self.response.out.write("""<script type="text/javascript" src="http://code.jquery.com/jquery-1.5.2.min.js"></script>
<script type="text/javascript" src="js/jquery.blockUI.js"></script>
<script type="text/javascript" src="js/slides.min.jquery.js"></script>
""")

def writeJavascript(self):
    weddingdate = db.GqlQuery("SELECT * FROM ImportantDates where name='weddingday'")
    d = weddingdate.get().date.strftime("%A %m/%d/%Y")
    self.response.out.write("""<script type="text/javascript">
        $(function() 
        {
            $('#why').click(function()
            {
                $('#answer').replaceWith("<div id=answer> it's at %s </div>");
                $('#why').replaceWith("<div id=why>need more <strong><a href="/details">details</a>???</strong></div><p>");
            });
        });
        
        </script>"""  % (d))
    self.response.out.write("""<script type="text/javascript">  
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



def writeDoctype(self):
    self.response.out.write("""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\r\n""")

def writeMeta(self):
  self.response.out.write("""<meta http-equiv="content-type" content="text/xhtml; charset=utf-8"/>\r\n<meta http-equiv="cache-control" content="no-cache"/>\r\n""")

def writeHeader(self):
  writeDoctype(self)
  self.response.out.write("""<html xmlns="http://www.w3.org/1999/xhtml">\r\n""")
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
            self.response.out.write("""<div id="why"><a href="#">find out why</a>...""")
        
        writeTracker(self)

        self.response.out.write("</body>")

class DetailsHandler(webapp.RequestHandler):
    def get(self):
        writeDoctype(self)
        self.response.out.write("""<html xmlns="http://www.w3.org/1999/xhtml">\r\n""")
        self.response.out.write("""<head>\r\n""");
        writeMeta(self)
        writeJQuery(self)
        writeJavascript(self)
        self.response.out.write("""<link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />""")
        self.response.out.write("""<title>Seriously, are they married yet?</title>\r\n""")
        self.response.out.write("""</head>\r\n\r\n""");
        self.response.out.write("<body>")
        self.response.out.write("""
                        <div id="container">
                            <div id="example">
                                <div id="slides">
                                    <div class="slides_container">
                                    <a href="#" title="Ride the Corinth Canal!" target="_blank"><img src="img/canal.jpg" width="570" height="450" alt="A n S in Corinth"></a>
                                    <a href="#" title="FishyFishyFishy" target="_blank"><img src="img/monterey.jpg" width="570" height="450" alt="Dont get eaten by fishes"></a>
                                    <a href="#" title="Happy Bokeh raining Day | Flickr - Photo Sharing!" target="_blank"><img src="http://slidesjs.com/examples/standard/img/slide-3.jpg" width="570" height="300" alt="Slide 3"></a>
                                    <a href="http://www.flickr.com/photos/b-tal/117037943/" title="We Eat Light | Flickr - Photo Sharing!" target="_blank"><img src="http://slidesjs.com/examples/standard/img/slide-4.jpg" width="570" height="300" alt="Slide 4"></a>
                                    <a href="http://www.flickr.com/photos/bu7amd/3447416780/" title="ÒI must go down to the sea again, to the lonely sea and the sky; and all I ask is a tall ship and a star to steer her by.Ó | Flickr - Photo Sharing!" target="_blank"><img src="http://slidesjs.com/examples/standard/img/slide-5.jpg" width="570" height="300" alt="Slide 5"></a>
                                    <a href="http://www.flickr.com/photos/streetpreacher/2078765853/" title="twelve.inch | Flickr - Photo Sharing!" target="_blank"><img src="http://slidesjs.com/examples/standard/img/slide-6.jpg" width="570" height="300" alt="Slide 6"></a>
                                    <a href="http://www.flickr.com/photos/aftab/3152515428/" title="Save my love for loneliness | Flickr - Photo Sharing!" target="_blank"><img src="http://slidesjs.com/examples/standard/img/slide-7.jpg" width="570" height="300" alt="Slide 7"></a>
                                </div>
                                <a href="#" class="prev"><img src="img/arrow-prev.png" width="24" height="43" alt="Arrow Prev"></a>
                                <a href="#" class="next"><img src="img/arrow-next.png" width="24" height="43" alt="Arrow Next"></a>
                            </div>
                            <img src="img/frame.png" width="739" height="450" alt="Frame" id="frame">
                        </div>
                    </div>""")
        self.response.out.write("""\r\n\r\n
            <div class="colmask rightmenu">
                <div class="colleft">
                    <div class="col1">
                        <div id="ptxt">
                            <a href="/">
                                <img src="img/sm_frame.png" id="sm_frame">
                                <img src="img/rose.jpg">
                            </a>
                            <p>Where
                        </div>
                    </div>
                    <div class="col2">
                        <div id="ptxt">
                            <a href="/">
                                <img src="img/sm_frame.png" id="sm_frame">
                                <img src="img/where.jpg">
                            </a>
                            <p>When
                        </div>
                    </div>
                    <div class="col3"> 
                        <div id="ptxt">
                            <a href="/">
                                <img src="img/sm_frame.png" id="sm_frame">
                                <img src="img/nextstop.jpg">
                            </a>
                            <p>Where to next??
                        </div>
                    </div>
                </div>
            </div>""")
        self.response.out.write("</body>")
        
class CreateHandler(webapp.RequestHandler):
    def get(self):
        a=ImportantDates()
        a.name='weddingday'
        a.date=datetime.date(2011,11,12)
        a.put()
        

def main():
    application = webapp.WSGIApplication([('/', MainHandler),
                                          ('/details',DetailsHandler),
                                          ('/createstuff',CreateHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()

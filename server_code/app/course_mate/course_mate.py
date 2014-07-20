import webapp2
import jinja2
import os

template_dir = os.path.join( os.path.dirname(__file__), 'templates' ) # makes templates visible
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw ):
        self.response.write(*a, **kw)
        
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params) # this render call is not same as below
    
    def my_render(self, template, **kw):
        self.write(self.render_str(template, **kw))
    

class Index(Handler):
    def get(self):
        self.my_render('index.html')
        #self.response.headers['Content-Type'] = 'text/plain'
        #self.response.write('Hello, World!')

    def post(self):
        faculty = self.request.get('faculty')
        self.my_render('index.html', error=faculty + " does not fucking exist")
    

app = webapp2.WSGIApplication(
                                [('/index', Index)    
                                ]
                                ,debug=True)    
import webapp2
import jinja2
import os
import sys

from google.appengine.ext import db
from google.appengine.api import memcache

from app_scripts.visualize_program import *
from app_scripts.optimalsemester import *
from app_scripts.possible_schedules import *
from app_scripts.vsb_url import *

from app_data.program_titles import *
from app_data.program_graph import *
from app_data.course_database import *
from app_data.teacher_data import *

from utils import *

template_dir = os.path.join( os.path.dirname(__file__), 'templates' ) # makes templates visible:
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)
    

class Users(db.Model):
    username = db.StringProperty(required = True)
    password_hash = db.StringProperty(required = True)
    email = db.EmailProperty(required = True)


class Handler(webapp2.RequestHandler):
    def isloggedIn(self):
        user_id_str = self.request.cookies.get('user_id')
        if user_id_str and check_secure_val(user_id_str):
            #return Users.get_by_id(int(user_id_str.split('|')[0]) ).username
            print True
            return True
        else:
            print False
            return False

    def write(self, *a, **kw ):
        self.response.write(*a, **kw)
        
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params) # this render call is not same as below
    
    def my_render(self, template, **kw):
        self.write(self.render_str(template, **kw))
    

class Index(Handler):

    def render_front(self, p = program_titles, error=''):
        loggedout = not(self.isloggedIn())
        self.my_render('index.html', loggedout=loggedout, maj=p, minor=p, error=error )
    
    def render_login_error(self, ue, pe):
        pass
        
    def render_signup_error(self, ue, pe, ve, ee):
        self.my_render('index.html', ue=ue, pe=pe, ve=ve, ee=ee)
        
    def p_schedule(self):
        major = self.request.get('major')
        minor = self.request.get('minor')
        minor2 = self.request.get('minor2')

        faculty = self.request.get('faculty')

        #self.render_front(error = "At the very minimum select a Major!")
        #self.render_front(welcome="Welcome to our wonderful service " + username + "!")
        self.redirect('/interface?major=' + major)
        
    def p_signup(self):
        d_username = self.request.get('d_username')
        d_password = self.request.get('d_password')
        verify = self.request.get('verify')
        d_email = self.request.get('d_email')
        
        usernames = [usr.username for usr in db.GqlQuery('SELECT * FROM Users')]
        
        if v_u(d_username, usernames) & v_pw(d_password) & v_vpw(verify,d_password) & v_em(d_email):
            new_user = Users(username = d_username, password_hash = make_pw_hash(d_username, d_password) , email=d_email)
            key = new_user.put()
    
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.headers.add_header('Set-Cookie', 'user_id=%s;Path=/' % make_secure_val(str(int(key.id()) ) ) )
            self.response.headers['Content-Type'] = 'text/html'
            time.sleep(1)
            self.render_front( )
            
        else:
            ue,pe,ve,ee = "Sorry, that username is taken!" if usrn_taken(d_username,usernames) else "Invalid Username" ,"Invalid Password","Passwords Don't Match","Invalid Email"
            self.render_signup_error(ue if not(v_u(d_username,usernames)) else "",  pe if not(v_pw(d_password)) else "",  ve if not(v_vpw(verify,d_password)) else "",  ee if not(v_em(d_email)) else "")
        
    def p_login(self):
        username = self.request.get('username')
        password = self.request.get('password')
        
        exists = db.GqlQuery("Select %s FROM Users" % username)
        
    def p_logout(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.headers.add_header('Set-Cookie', 'user_id=;Path=/')
        self.response.headers['Content-Type'] = 'text/html'
        self.render_front( )
        
    def get(self):
        self.render_front( )

    def post(self):
        is_get_schedule = self.request.get('get_schedule')
        is_login = self.request.get('login')
        is_signup = self.request.get('signup')
        is_logout = self.request.get('logout')
        
        if is_get_schedule:
            self.p_schedule()
            
        elif is_login:
            self.p_login()
            
        elif is_signup:
            self.p_signup()
            
        elif is_logout:
            self.p_logout()
        
class Interface(Handler):
    
    def render_interface(self, nodes, edges, optimalfall, optimalwinter , url):
        self.my_render('interface.html', nodes=nodes, edges=edges, optimalfall=optimalfall, optimalwinter=optimalwinter, url=url)

    def get(self):
        major = self.request.get('major')
        nodes, edges = visualize(major, program_graph, course_database)
        
        possibilites = gen_possible_schedules(course_database, program_graph[major] )
        osched = optimal(course_database, possibilites, teacher_data)
        url = get_vsb_url(course_database, osched)
    
        self.render_interface(nodes, edges, osched, osched, url )

app = webapp2.WSGIApplication(  [('/index', Index),  
                                 ('/interface', Interface)
                                 ]
                                ,debug=True)    
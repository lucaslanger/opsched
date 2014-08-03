import re
import hmac
import random
import hashlib
import string
import time

SECRET = 'hansweisurikaslovgibankaboul'

def make_salt():
    return ''.join(random.choice(string.letters) for x in xrange(5))

def make_pw_hash(name, pw, salt = None):
    if salt == None:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s|%s' % (h, salt)

def valid_pw(name, pw, h):
    if make_pw_hash(name, pw, h.split('|')[1]) == h:
        return True
    return False	
	
def hash_str(s):
	return hmac.new(SECRET,s).hexdigest()
	
def make_secure_val(s):
	return '%s|%s' % (s, hash_str(s))
	
def check_secure_val(h):
	val = h.split('|')[0]
	if make_secure_val(val) == h:
		return val
	else: 
		return None

def usrn_taken(u, liusers):
	if u in liusers:
		return True
	return False
	
def v_u(s, usernames):
	if usrn_taken(s, usernames):
		return False
	elif re.match(r"^[a-zA-Z0-9_-]{3,20}$",s) != None:
		return True
	else:
		return False
def v_pw(s):
	if re.match(r"^.{3,20}",s) != None:
		return True
	else:
		return False
def v_vpw(s,pw):
	if s == pw:
		return True
	else: 
		return False
def v_em(s):
	if re.match(r"^[\S]+@[\S]+\.[\S]+$",s) != None or s == "":
		return True
	else:
		return False
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 29 01:10:10 2014

@author: Lucas
"""

import web

urls = ( 
    '/', 'index'
)

class index:
    def GET(self):
        return "Hello World!"
        
if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()


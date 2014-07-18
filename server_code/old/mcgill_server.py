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
        render = web.template.render('templates/')
        return render.index()
        
if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()


#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi
import re

# html boilerplate for the top of every page
page_header = """
<!DOCTYPE html>
<html>
<head>
    <style>
    body {
        font-family: arial, sans-serif;
    }
    h1 {
        font-size: 1.5em;
        text-align: center;
    }
    h2 {
        font-size: 1.2em;
        text-align: center;
    }
    form {
        background-color:#eee;
        padding: 30px;
        border: 1px #333 solid;
        margin: 30px auto;
        width:500px;
    }
    input {
        padding: 5px 0;
        margin: 5px 0;
    }
    .error {
        color: red;
        font-size: .9em;
    }
    </style>
    <title>User Signup</title>
</head>
<body>
"""

#page header
edit_header = "<h1>LaunchCode: Formation Assignment</h1><h2>User Signup</h2>"

# a form for adding text
form = """
<form method="post">
    Username <input type="text" name="username" value="%(un)s"> <span class="error">%(error_un)s</span>
    <br />
    Password <input type="password" name="password"> <span class="error">%(error_pw)s</span>
    <br />
    Verify Password <input type="password" name="verify">
    <br />
    Email (optional) <input type="text" name="email" value="%(email)s"> <span class="error">%(error_email)s</span>
    <br /><br />
    <input type="submit" value="Create My Account"/>
</form>
"""


# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""

class MainHandler(webapp2.RequestHandler):
    def write_form(self, un="", email="", error_un="", error_pw="",error_email=""):
        # combine all the pieces to build the content of our response
        main_content = edit_header + form
        response = page_header + main_content + page_footer
        #self.response.write(response % {"error": error, "encrypted": encrypted})
        self.response.write(response % {"un": un, "email": email, "error_un": error_un, "error_pw": error_pw, "error_email": error_email})

    def get(self):
        self.write_form()

    def post(self):
        #methods to validate input fields are valid
        USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        def valid_username(username):
            return USER_RE.match(username)

        PW_RE = re.compile(r"^.{3,20}$")
        def valid_pw(password):
            return PW_RE.match(password)

        EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
        def valid_email(email):
            return not email or EMAIL_RE.match(email)

        #get form field data
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        #verify username entered
        if not valid_username(username):
            self.write_form(username, email, "Please enter a valid username","","")
        else:
            #verify passwords are valid and matching
            if not valid_pw(password):
                self.write_form(username, email, "","Please enter a valid password","")
            else:
                if password != verify:
                    self.write_form(username, email, "","Passwords do not match","")
                else:
                    if not valid_email(email):
                        self.write_form(username, email, "","","Please enter a valid email")
                    else:
                    #redirect to welcome page
                        self.redirect("/welcome?username=" + username)


class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        username = self.request.get("username")
        self.response.write("Welcome, " + username + "!!")

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', WelcomeHandler)
], debug=True)

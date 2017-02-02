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

def valid_username(name):
    if not re.match(r"^[a-zA-Z0-9_-]{3,20}$", name):
        return False
    else:
        return True

def valid_password(password):
    password_len = int(len(password))
    if password_len > 2 and password_len < 21:
        if not re.search(r"^.{3,20}$", password):
            return False
        else:
            if re.match(r"^.{3,20}$", password):
                return True
            else:
                return False
    else:
        return False

def valid_email(email):
    if not re.match(r"^[\S]+@[\S]+.[\S]+$", email):
        return False
    else:
        return True

def valid_passwords(password1, password2):
	if password1 == password2:
		return True
	else:
		return False
form = """<form method= "post">
		<h1>Signup</h1>
			<table>
				<tbody>
					<tr>
						<td><lable for="username">Username</label></td>
						<td><input type= "text" name= "username" value = "%(username)s"/></td>
						<td><span style = "color:red">%(error_username)s</span></td>
					</tr>
					<tr>
						<td><lable for="password">Password</label></td>
						<td><input type= "password" name= "password"/></td>
						<td><span style = "color:red">%(error_password)s</span></td>

					</tr>
					<tr>
						<td><lable for="verify">Verify Password</label></td>
						<td><input type= "password" name= "verify"/></td>
						<td><span style = "color:red">%(error_verify)s</span></td>

					</tr>
					<tr>
						<td><lable for="email">Email (optional)</label></td>
						<td><input type= "text" name= "email" value = "%(email)s"/></td>
						<td><span style = "color:red">%(error_email)s</span></td>

					</tr>
				</tbody>
			</table>
		<br>
		<br>
		<input type="submit"/>
		</form>"""

class MainHandler(webapp2.RequestHandler):
    def write_form(self, user="", mail="", e_user="", e_pas="", e_pasw="", e_email=""):
    	self.response.out.write(form % {"username": user, "email": mail, "error_password": e_pas, "error_username": e_user, "error_verify": e_pasw, "error_email": e_email })

    def get(self):

        self.write_form()

    def post(self):
    	user = self.request.get("username")
    	pas = self.request.get("password")
    	pas_v = self.request.get("verify")
    	mail = self.request.get("email")
    	e_user = ""
    	e_pas = ""
    	e_pasw = ""
    	e_email = ""

    	v_user = valid_username(user)
    	if v_user == False:
    		e_user +=  "Username not valid"

        v_pas = valid_password(pas)
    	if v_pas == False:
    		e_pas += "Password not valid"

    	v_pasw = valid_passwords(pas, pas_v)
    	if v_pasw == False:
    		e_pasw += "Passwords don't match"

    	v_email = valid_email(mail)
    	if v_email == False:
    		e_email += "This is not a Valid Email!!!"


    	if v_user and v_pas and v_pasw :
    		self.redirect("/welcome")
    	else:
    		self.write_form(cgi.escape(user), cgi.escape(mail), e_user, e_pas, e_pasw, e_email)


class Welcome(webapp2.RequestHandler):
    def get(self):
        username = self.request.get("username")
        self.response.write("<h1>Welcome !!! " + username + "</h1>")


app = webapp2.WSGIApplication([
    ('/', MainHandler),('/welcome', Welcome)
], debug=True)

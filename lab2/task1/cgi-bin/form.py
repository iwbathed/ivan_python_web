#!/usr/bin/env python3

from http import cookies
import os
import cgi

form = cgi.FieldStorage()
university = form.getfirst("university", "Default university value")
faculty = form.getfirst("faculty", "Default faculty value")
if form.getvalue("dropdown"):
    course = form.getvalue("dropdown")
else:
    course = 'Not chosen'
subjects = [
            form.getvalue("math"),
            form.getvalue("physics"),
            form.getvalue("artificial intelligence"),
            form.getvalue("web development")
            ]

cookie = cookies.SimpleCookie(os.environ["HTTP_COOKIE"])
if "form_counter" in cookie:
    cookie_am = cookie.get("form_counter").value
    print(f"Set-cookie: form_counter={int(cookie_am) + 1}")
else:
    cookie_am = "1"
    print("Set-cookie: form_counter=1")


def subjects_show(subjects):
    res = ""
    for i in subjects:
        if i:
            res += f"<p>{i}</p>"
    if not res:
        res = "<p>Not chosen</p>"
    return res

HTML = f'''<!DOCTYPE html>
<html lang="en-US">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width" />
    <title>Task 1</title>
  </head>
  <body>
  <p>University: {university}</p>
  <p>Faculty: {faculty}</p>
  <p>Course: {course}</p>
  <p>Subjects to study:</p>
  {subjects_show(subjects)}
  <p>Cookie counter : {cookie_am}</p>
  </body>
</html>'''

print("Content-type: text/html\r\n\r\n")
print()
print(HTML)


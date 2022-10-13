<h1 align="center"> Simple Flask Blog 

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
</h1>

<p align="center">
Simple Flask Blog is a blog written with flask & jinja 
</p>

<h2>
Setup Project :
</h2>

---

<h3>
Using Dockerfile
</h3>

<p>
First of all fill all required ENV for Dockerfile
</p>

```docker
ENV SECRET_KEY='YOUR SECRETKEY'
ENV SQLALCHEMY_DATABASE_URI='sqlite:///site.db'

ENV MAIL_SERVER='SMTP MAIL SERVER'
ENV SMTP_PORT='SMTP PORT'

ENV MAIL_USERNAME='SMTP USER'
ENV MAIL_PASSWORD='SMTP PASS'
```
<p>
Save Dockerfile . then build image
</p>

```sh
docker build -t flask-app:1.0 .
```
<p>
Now run image :
</p>

```sh
docker run -p 80:80 flask-app:1.0
```

---

<h3>
Without Docker (Advanced Way)
</h3>

<p>
First you need to Create a VENV for the Project
Open a Terminal in Project Directory and use Below line to Create VENV:
</p>
<div dir="ltr">
<pre>
python3 -m venv venv
</pre>
</div>
<p>
Now you have to Activate VENV<br>
For Activating VENV use below line :
</p>
<b>
Linux/macOS:
</b>
<div dir="ltr">
<pre>
source venv/bin/activate
</pre>
</div>
<b>
Windows:
</b>
<div dir="ltr">
<pre>
venv/Scripts/activate.ps1
</pre>
</div>
<br>
<p>
After Activating VENV you have to install <strong>requirements.txt</strong>
</p>
<div dir="ltr">
<pre>
pip3 install -r requirements.txt
</pre>
</div>

<h4>
Set Environment Variables:
</h4>

```bash
export SECRET_KEY='Your Secret Key'
export SQLALCHEMY_DATABASE_URI='sqlite:///site.db'
export MAIL_SERVER='SMTP Server URL'
export SMTP_PORT='SMTP PORT'
export MAIL_USERNAME='SMTP USERNAME'
export MAIL_PASSWORD='SMTP PASSWORD'
```

<b>
Note:
</b>
<p>
 save above exports to .bashrc for holding the values to your default shell.
</p>

<h4>
Initial Database and admin user :
</h4>

```python
python3 dbinit.py
```

<b>
Note:
</b>
<p>
  Before using above command make sure to edit <strong>dbinit.py</strong> for changing blogname , navbar and admin information to your needs.
</p>


<h4>
Run Project :
</h4>
<p>
Enter this command in the terminal to run the project :
</p>
<div dir="ltr">
<pre>
python3 -m flask run --port 80
</pre>
</div>

<p>
Now enter the given address in the URL bar of your browser:
</p>
<div dir="ltr">
<pre>
http://127.0.0.1:80/
</pre>
</div>

<b>
Note:
</b>
<p>
  Default admin username and password are :
</p>

```text
Email : admin@gmail.com  
Password : admin
```

---

<h2>
Config Project :
</h2>

<p>
  Open <strong>app/config.py</strong> with you desired editor.
  
  if you want to disallow anyone to register and write post change :
 <div dir="ltr">
<pre>
USER_REGISTER = True
</pre>
   to <strong>False</strong>.
</p>

---

<p><strong> This Project are still in development so i wrote a todo list to track the Progress</strong></p>

<h3> Todo List </h3>

- [x] Better Structure of Application
- [x] Add Database to Application
- [x] Add A Way To Create,Update,Delete Posts with Privileged User 
- [x] User Account , Profile Picture
- [x] User Password Encryption (brcypt method used)
- [ ] A Better Post Edit Section with Markdown or JS
- [x] Code Refactoring & Cleaner Code
- [x] Blueprints
- [x] Custom Error Pages
- [x] Cache Exeptions to Show Error Pages
- [x] Dockerfile

[contributors-shield]: https://img.shields.io/github/contributors/SonyaCore/simple-flask-blog?style=for-the-badge
[contributors-url]: https://github.com/SonyaCore/simple-flask-blog/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/SonyaCore/simple-flask-blog?style=for-the-badge
[forks-url]: https://github.com/SonyaCore/simple-flask-blog/network/members
[stars-shield]: https://img.shields.io/github/stars/SonyaCore/simple-flask-blog?style=for-the-badge
[stars-url]: https://github.com/SonyaCore/simple-flask-blog/stargazers
[issues-shield]: https://img.shields.io/github/issues/SonyaCore/simple-flask-blog?style=for-the-badge
[issues-url]: https://github.com/SonyaCore/simple-flask-blog/issues


<h1 align="center" >
Flask-Blog 
</h1>
<p align="center">
A Simple Flask Blog (Still in Development)
</p>

<h3>
Setup Project :
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

---

<h3>
Run Project :
</h3>
<p>
Enter this command in the terminal to run the project :
</p>
<div dir="ltr">
<pre>
python3 run.py
</pre>
</div>

<p>
Now enter the given address in the URL bar of your browser:
</p>
<div dir="ltr">
<pre>
http://127.0.0.1:8080/
</pre>
</div>

---
<p><strong> This Project are still in development so i wrote a todo list to track the Progress</strong></p>

<h3> Todo List </h3>

- [x] Better Structure of Application
- [x] Add Database to Application
- [x] Add A Way To Create,Update,Delete Posts with Privileged User 
- [x] User Account , Profile Picture
- [x] User Authentication (brcypt method used)
- [ ] A Better Post Edit Section with Markdown or JS
- [ ] Code Refactoring & Cleaner Code
- [x] Blueprints
- [ ] Custom Error Pages
- [ ] Cache Exeptions to Show Error Pages
- [ ] Dockerfile

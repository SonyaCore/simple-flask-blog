from flask import Flask , render_template , url_for, flash , redirect
from forms import RegistrationForm , LoginForm
from API import APIKEY

app = Flask(__name__)
app.config['SECRET_KEY'] = APIKEY

main_post = [
    {
        'author': 'sonya',
        'date_posted': '2022-04-20',
        'title': 'flask-api',
        'content': '''Flask is a micro web framework written in Python. It is classified as a microframework because it does not require particular tools or libraries.It has no database abstraction layer, form validation, or any other components where pre-existing third-party libraries provide common functions. However, Flask supports extensions that can add application features as if they were implemented in Flask itself. Extensions exist for object-relational mappers, form validation, upload handling, various open authentication technologies and several common framework related tools.'''
    },
]

# Additional Navbar Information
@app.context_processor
def layout():
    url = {
        'github':      'https://github.com/SoniaCore',
        'telegram':    'https://telegram.me/ReiLibre',
        'info':        'Still in Development @SoniaCore',
    }
    return dict(url=url)

# Blog Name
@app.context_processor
def name():
    info = {
        'servername':   'Sonia Blog'
    }
    return dict(info=info)

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html',posts=main_post)

@app.route('/about')
def calc():
    return render_template('about.html')

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'{form.username.data} created !', 'success')
        return redirect(url_for('home'))
    return render_template('register.html',title='Register', form = form)

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html',title='Login', form = form)

if __name__ == '__main__':
    app.run(debug=True , port=8080)
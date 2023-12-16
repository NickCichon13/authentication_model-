from flask import Flask, redirect, render_template, flash, session
from models import db, connect_db, User, Feedback
from forms import UserForm, UserLogin, UserFeedback

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///demo_web123"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abcd1234hjhggfg"
app.app_context().push()

connect_db(app)
db.create_all
 
@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/register', methods=['GET','POST'])
def register_user():
     form = UserForm()
     if form.validate_on_submit():
          username = form.username.data
          email = form.email.data
          password = form.password.data
          first_name = form.first_name.data
          last_name = form.last_name.data
          print("first_name", first_name)
          new_user = User.register(username,email, password, first_name, last_name)
          print("User.register", User.register)
          print("new_user", new_user)
        
          db.session.add(new_user)
          db.session.commit()
          flash("Welcome You created your user in this crazy world")
          return redirect('/')
     
     return render_template('register.html', form=form)

@app.route('/secret')
def secret_page():
     if "username" not in session:
          return redirect('/')
     else:
          user = User.query.all()
          return render_template('secret.html',user=user)

@app.route('/login', methods=['GET','POST'])
def loging_user():
     form = UserLogin()
     if form.validate_on_submit():
          username = form.username.data
          password = form.password.data
          user = User.authenticate(username,password)
          if user:
               session['username'] = user.username
               return redirect('/secret')
          else:
               form.username.errors = ['Invalid Username/Password']
     
     return render_template('login.html', form=form)

@app.route('/logout')
def logout_user():
     session.pop('username')
     return redirect('/')

@app.route('/users/<username>', methods=['GET','POST'])
def show_info(username):
     
     if 'username' not in session:
          flash("You need to log in first")
          return redirect('/login')
     form = UserForm()
     user = User.query.get(username)
     

     return render_template('information.html', form=form, user=user)

@app.route('/feedbacks', methods=['GET','POST'])
def creat_feedback():
     if 'username' not in session:
          flash('you must login first')
          return redirect('/login')
     form= UserFeedback()
     all_feedback = Feedback.query.all()
     if form.validate_on_submit():
          title = form.title.data
          content = form.content.data

          new_feedback = Feedback(title=title,content=content)
          db.session.add(new_feedback)
          db.session.commit()
          flash('you have created a Feedback! Thank you!')
          return redirect('/feedbacks')

     return render_template('information.html', form=form, feedbacks=all_feedback)

@app.route('/feedbacks/<username>/delete', methods=['POST'])
def delete_feedback(username):
     if username not in session:
          flash("you don't have the right to do that!")
          return redirect('/login')
     feedback = Feedback.query.get_or_404(username)
     if feedback.username == session['username']:
          db.session.delete(feedback)
          db.session.commit()
          flash('Feedback was deleted')
          return redirect('/feedbacks')

@app.route('/feedbacks/<int:feedback_id>/edit', methods=['POST'])
def edit_feedback(feedback_id):
     feedback = Feedback.query.get(feedback_id)

     if 'username' not in session:
          flash("you dont have authority to update another users message")
          return redirect('/login')
     form = Feedback(obj=feedback)

     if form.validate_on_submit():
          feedback.title =form.title.data
          feedback.content = form.content.data

          db.session.commit()

          return redirect('/users/feedbacks')
     
     return render_template('/feedbacks/edit.html', form=form, feedback=feedback)

    
if __name__ == "__main__":
     app.run(debug=True)
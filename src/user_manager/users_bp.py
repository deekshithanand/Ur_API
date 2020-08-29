# create bp routes here

from flask import Blueprint, request, render_template, flash, redirect, url_for, current_app as app
from flask_login import login_user, logout_user, login_required, current_user
from .forms import *
from werkzeug.security import generate_password_hash, check_password_hash
from src import mongo
from src.dUtils import generateToken, verify_token
from .loginmanager import Users, lm
import uuid
from base64 import urlsafe_b64decode, urlsafe_b64encode
import hmac
from hashlib import sha256

user_manager_bp = Blueprint('user_manager', __name__, template_folder="templates",
                            static_folder='static', static_url_path='/user_manager/static')

# define the routes here
# all api calls are after v1


def deprecateTokenfromDB(duuid: "str", apiString):
    # remove from uuid
    mongo.db.UuidMapper.delete_one(
        {
            "uuid": duuid
        }
    )
    mongo.db.UserBase.update_one({"email_id": current_user.get_id()},
                                 {"$pull": {"api_string": apiString}}
                                 )


@user_manager_bp.route('/login', methods=['GET', 'POST'])
def dlogin():

    form = UserLogin(request.form)

    if request.method == 'GET':

        return render_template('login.html', form=form)

    if request.method == "POST":

        if form.validate():

            user = mongo.db.UserBase.find_one(
                {"email_id": form.email_id.data}, {'_id': 0})

            if user:
                if check_password_hash(user['pwd_hash'], form.password.data):

                    # create a user object and load
                    usr = Users(user['email_id'])
                    login_user(usr)
                    flash("Login Successfull!", 'success')
                    next = request.args.get('next')
                    return redirect(next or url_for('user_manager.dindex'))
                else:
                    flash("Incorrect Password!", 'danger')
                    return render_template('login.html', form=form)
            else:
                flash("User Doesn't Exist!", 'danger')
                return render_template('login.html', form=form)
        else:
            print(form.errors)
            return render_template('login.html', form=form)


@user_manager_bp.route('/gen_token', methods=['POST'])
@login_required
def gen_token():
    api_key, duuid = generateToken(app.config['SECRET_KEY'])
    new_umapper = {
        "uuid": duuid,
        "usr_id": current_user.get_id()
    }
    mongo.db.UuidMapper.insert_one(new_umapper)

    # update_user_base:
    query = {"email_id": new_umapper['usr_id']}
    update_val = {"$push": {"api_string": api_key[:10]}}
    err = mongo.db.UserBase.update_one(
        query,
        update_val
    )
    flash("New API Key is created!", 'success')
    return render_template("apikey.html", key=api_key)


@user_manager_bp.route("/revoke_token", methods=['POST'])
@login_required
def revoke_token():
    # accept api_string and
    user_string = request.form.get("AS")

    # get all records from uuid mapper!
    records = mongo.db.UuidMapper.find({
        "usr_id": current_user.get_id()
    }, {"_id": 0})

    for record in records:
        token, duuid = generateToken(app.config['SECRET_KEY'], record["uuid"])
        a = record["uuid"] == duuid
        if user_string == token[:10]:
            deprecateTokenfromDB(record["uuid"], user_string)
            flash("API Deprecrated!", 'success')
            break
    else:
        flash("Api_Key Error", 'warning')

    return redirect(url_for("user_manager.dindex"))


@user_manager_bp.route('/',)
@login_required
def dindex():
    # define home page here get user details here
    # display token only the first 10 cahrs
    # revoke token
    # display data
    email_id = current_user.get_id()
    api_string = mongo.db.UserBase.find_one({"email_id": email_id}, {"_id": 0})

    return render_template('index.html', akeys=api_string['api_string'])


@user_manager_bp.route('/logout')
@login_required
def dlogout():
    logout_user()
    # flash message here
    return "User Logged out successfully!"


@user_manager_bp.route('/register', methods=['GET', 'POST'])
def dregister():
    # create new user credentials here
    form = UserSignup(request.form)

    if request.method == 'GET':
        return render_template('register.html', form=form)

    if request.method == 'POST':
        # chek in db if exists
        # create record in Payloads and in UserBase
        # flash success
        # redirect to login
        if form.validate():
            db = mongo.db.UserBase
            new_email_id = form.email_id.data
            user_exists = db.find_one({"email_id": new_email_id})

            if user_exists:
                # user exists error
                flash("Mail ID Already Taken!", 'danger')
                return render_template('register.html', form=form)

            else:
                # create userbase and payload entries
                new_user = dict()
                new_user["email_id"] = new_email_id
                new_user['pwd_hash'] = generate_password_hash(
                    form.password.data)
                new_user['api_string'] = []

                db.insert_one(new_user)
                del new_user['pwd_hash']
                del new_user['api_string']

                mongo.db.Payload.insert_one(new_user)

                flash("New User Created!", 'success')
                return redirect(url_for("user_manager.dlogin"))
        else:
            return render_template('register.html', form=form)


# @user_manager_bp.route('/test/')
# def test_template(name=None):
#     return "pass"

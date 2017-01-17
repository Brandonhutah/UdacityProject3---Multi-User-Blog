from google.appengine.ext import db
import hmac
import hashlib
import re
import random
from string import letters

SECRET = "ThisIsASecret"


class User(db.Model):
    name = db.StringProperty(required=True)
    pw_hash = db.StringProperty(required=True)
    email = db.StringProperty(required=False)


def make_secure_hash(val):
    return "%s|%s" % (val, hmac.new(SECRET, str(val)).hexdigest())


def get_logged_in_user(request):
    hash = request.cookies.get("userId")

    if hash and hash.split("|")[0]:
        id = hash.split("|")[0]
        user = User.get_by_id(int(id))

        if hash == make_secure_hash(int(id)) and user:
            return user


def valid_Username(name):
    USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    return USER_RE.match(name)


def valid_Password(password):
    PASS_RE = re.compile(r"^.{3,20}$")
    return PASS_RE.match(password)


def valid_Email(email):
    EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
    return EMAIL_RE.match(email)


def make_salt(length=5):
    return ''.join(random.choice(letters) for x in xrange(length))


def make_pw_hash(name, pw, salt=""):
    if not salt:
        salt = make_salt()
    return hashlib.sha256(name + pw + salt).hexdigest() + "|" + salt


class VerifyErrors():
    userError = ""
    passError = ""
    verifyError = ""
    emailError = ""


def user_already_exists(userName):
    return User.all().filter('name =', userName).get()


def verify_data(username, password, verify, email=""):
    errors = VerifyErrors()
    userError = ""
    passError = ""
    verifyError = ""
    emailError = ""

    if not valid_Username(username) or user_already_exists(username):
        userError = "That's not a valid username or name already exists."
    if not valid_Password(password):
        passError = "That's not a valid password."
    if password != verify:
        verifyError = "Passwords do not match."
    if email:
        if not valid_Email(email):
            emailError = "That's not a valid email."
    if userError or passError or verifyError or emailError:
        errors.userError = userError
        errors.passError = passError
        errors.verifyError = verifyError
        errors.emailError = emailError
        return errors


def create_account(username, password, email=""):
    newHash = make_pw_hash(username, password)
    newUser = User(name=username, pw_hash=newHash, email=email)
    newUser.put()
    return newUser.key().id()

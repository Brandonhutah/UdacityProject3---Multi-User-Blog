import page_handler
import account_handler


class GatewayPage(page_handler.Handler):

    def get(self):
        user = account_handler.get_logged_in_user(self.request)
        if user:
            self.response.headers.add_header("Set-Cookie", "userId=; Path=/")
            self.redirect("/")
        else:
            self.render("gatewaypage.html")

    def post(self):
        if self.request.get("createSubmit"):
            username = self.request.get("username")
            password = self.request.get("password")
            verify = self.request.get("verify")
            email = self.request.get("email")

            errors = account_handler.verify_data(
                username, password, verify, email)
            if not errors:
                userId = account_handler.create_account(
                    username, password, email)
                self.response.headers.add_header(
                    "Set-Cookie", "userId=" + account_handler.make_secure_hash(userId) + "; Path=/")
                self.redirect("/")
            else:
                self.render("gatewaypage.html",
                            createUsername=username,
                            createEmail=email,
                            createUserError=errors.userError,
                            createPassError=errors.passError,
                            createVerifyError=errors.verifyError,
                            createEmailError=errors.emailError)
        if self.request.get("loginSubmit"):
            username = self.request.get("username")
            password = self.request.get("password")

            user = account_handler.user_already_exists(username)
            if user:
                salt = user.pw_hash.split("|")[1]
                if user.pw_hash == account_handler.make_pw_hash(username, password, salt):
                    self.response.headers.add_header(
                        'Set-Cookie', 'userId=' + account_handler.make_secure_hash(user.key().id()) + '; Path=/')
                    self.redirect("/")
                else:
                    self.render("gatewaypage.html", loginUsername=username,
                                loginUserError="Invalid username or password")
            else:
                self.render("gatewaypage.html", loginUsername=username,
                            loginUserError="Invalid username or password")

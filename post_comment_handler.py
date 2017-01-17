import page_handler
import account_handler
import db_handler
import datetime


def has_user_liked_post(name, users):
    """method determines if a user has liked a post
            Arg:
                    name: the username of the user currenty logged in
                    users: a comma seperated list of users that have liked a given post
            return:
                    true if user is in users
                    none otherwise
    """
    if users:
        users = users.split(",")
        for user in users:
            if name == user:
                return True


class NewPage(page_handler.Handler):

    def get(self, id=""):
        user = account_handler.get_logged_in_user(self.request)
        if user:
            if id:
                post = db_handler.get_post_by_id(int(id))
                if post:
                    self.render(
                        "newpage.html", title="New Comment Page", post=post)
                else:
                    self.redirect("/")
            else:
                self.render("newpage.html", title="New Post Page")
        else:
            self.redirect("/accountgateway")

    def post(self, id=""):
        user = account_handler.get_logged_in_user(self.request)
        type = self.request.get("action")
        if user:
            if type == "Comment":
                content = self.request.get("content")
                author = user.name
                postedToId = int(self.request.get("postId"))

                comment = db_handler.BlogComment(
                    content=content, author=author, postedToId=postedToId)
                db_handler.add_comment(comment)
                self.redirect("/" + str(postedToId))

            elif type == "Post":
                title = self.request.get("title")
                content = self.request.get("content")
                author = user.name

                newPost = db_handler.BlogPost(
                    title=title, content=content, author=author, likes=0)
                id = db_handler.create_new_post(newPost)
                self.redirect("/" + str(id))


class PostPage(page_handler.Handler):

    def get(self, postId):
        user = account_handler.get_logged_in_user(self.request)
        post = db_handler.get_post_by_id(postId)
        comments = db_handler.get_comments_for_post(postId)
        liked = False

        if user:
            liked = has_user_liked_post(user.name, post.liked_by_users)

        self.render("postpage.html", title=post.title,
                    post=post, comments=comments, liked=liked)


class EditPage(page_handler.Handler):

    def get(self, postId):
        user = account_handler.get_logged_in_user(self.request)
        if user:
            post = db_handler.get_post_by_id(int(postId))
            if post:
                if user.name == post.author:
                    self.render("editpage.html", title="Edit Post", post=post)
                else:
                    self.redirect("/" + postId)

            comment = db_handler.get_comment_by_id(int(postId))
            if comment:
                if user.name == comment.author:
                    self.render(
                        "editpage.html", title="Edit Comment", comment=comment)
                else:
                    self.redirect("/" + comment.postedToId)

    def post(self, postId):
        user = account_handler.get_logged_in_user(self.request)
        type = self.request.get("action")
        if user:
            if type == "Post":
                id = self.request.get("postId")
                post = db_handler.get_post_by_id(id)

                if post.author == user.name:
                    title = self.request.get("title")
                    content = self.request.get("content")

                    post.title = title
                    post.content = content

                    id = db_handler.update_post(post)
                    self.redirect("/" + str(id))
                else:
                    self.redirect("/" + str(id))

            if type == "Comment":
                id = self.request.get("commentId")
                comment = db_handler.get_comment_by_id(id)

                if comment.author == user.name:
                    content = self.request.get("content")

                    comment.content = content

                    db_handler.update_comment(comment)
                    self.redirect("/" + str(comment.postedToId))


class Delete(page_handler.Handler):

    def get(self, postId):
        user = account_handler.get_logged_in_user(self.request)
        if user:
            post = db_handler.get_post_by_id(int(postId))
            if post and post.author == user.name:
                db_handler.delete_post(post)
                self.redirect("/")

            comment = db_handler.get_comment_by_id(int(postId))
            if comment and comment.author == user.name:
                postId = comment.postedToId
                db_handler.delete_comment(comment)
                self.redirect("/" + str(postId))


class LikePost(page_handler.Handler):

    def get(self, postId):
        user = account_handler.get_logged_in_user(self.request)
        post = db_handler.get_post_by_id(int(postId))

        if user:
            if has_user_liked_post(user.name, post.liked_by_users):
                post.likes = post.likes - 1
                post.liked_by_users = post.liked_by_users.replace(
                    "," + user.name, "")
                db_handler.update_post(post)
                self.redirect("/" + postId)
            elif user.name != post.author:
                post.likes = post.likes + 1
                post.liked_by_users = str(
                    post.liked_by_users) + "," + user.name
                db_handler.update_post(post)
                self.redirect("/" + postId)
        else:
            self.redirect("/accountgateway")

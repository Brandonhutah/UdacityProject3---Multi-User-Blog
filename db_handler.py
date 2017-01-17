from google.appengine.ext import db


class BlogPost(db.Model):
    title = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    likes = db.IntegerProperty(required=True)
    liked_by_users = db.TextProperty(required=False)
    author = db.StringProperty(required=True)


class BlogComment(db.Model):
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    author = db.StringProperty(required=True)
    postedToId = db.IntegerProperty(required=True)


def add_comment(comment):
    comment.put()
    return comment.key().id()


def delete_comment(comment):
    comment.delete()


def update_comment(comment):
    comment.put()
    return comment.key().id()


def get_comments_for_post(postId):
    comments = db.GqlQuery("select * from BlogComment order by created desc")
    postComments = []
    if comments:
        for comment in comments:
            if str(comment.postedToId) == postId:
                postComments.append(comment)
    return postComments


def get_comment_by_id(commentId):
    return BlogComment.get_by_id(int(commentId))


def get_all_posts():
    return db.GqlQuery("select * from BlogPost order by created desc")


def get_post_by_id(postId):
    return BlogPost.get_by_id(int(postId))


def create_new_post(post):
    post.put()
    return post.key().id()


def update_post(post):
    post.put()
    return post.key().id()


def delete_post(post):
    post.delete()

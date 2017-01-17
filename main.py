import webapp2
import re
import page_handler
import gateway_page
import db_handler
import post_comment_handler


class MainPage(page_handler.Handler):

    def get(self):
        blog_posts = db_handler.get_all_posts()
        self.render("mainpage.html", title="Main Page", posts=blog_posts)


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/newpost', post_comment_handler.NewPage),
    ('/(\d+)', post_comment_handler.PostPage),
    ('/accountgateway', gateway_page.GatewayPage),
    ('/editpost/(\d+)', post_comment_handler.EditPage),
    ('/delete/(\d+)', post_comment_handler.Delete),
    ('/newComment/(\d+)', post_comment_handler.NewPage),
    ('/editComment/(\d+)', post_comment_handler.EditPage),
    ('/likePost/(\d+)', post_comment_handler.LikePost)
], debug=True)

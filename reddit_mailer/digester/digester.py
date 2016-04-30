import praw
from nameko.rpc import rpc
from nameko.rpc import RpcProxy

USER_AGENT = 'reddit_digester'


class Digester(object):
    name = "reddit_digester"
    mailer = RpcProxy("mailer")

    @rpc
    def digest(self, subreddit, limit, to):
        r = praw.Reddit(user_agent=USER_AGENT)
        submissions = r.get_subreddit(subreddit).get_top(limit=limit)
        text = "\n".join([str(s) for s in submissions])
        subject = "Top {} from /r/{}".format(limit, subreddit)
        self.mailer.send_digest(
            {"text": text, "subject": subject},
            to
        )

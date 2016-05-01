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
        context = {
            "r": subreddit,
            "limit": limit,
            "posts": [{
                "score": s.score,
                "permalink": s.permalink,
                "title": s.title
            } for s in submissions]
        }
        self.mailer.send_digest(context, to)

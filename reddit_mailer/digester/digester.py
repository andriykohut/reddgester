import praw
from nameko.rpc import rpc

USER_AGENT = 'reddit_digester'


class Digester(object):
    name = "reddit_digester"

    @rpc
    def digest(self, subreddit, limit):
        r = praw.Reddit(user_agent=USER_AGENT)
        submissions = r.get_subreddit(subreddit).get_hot(limit)
        return submissions

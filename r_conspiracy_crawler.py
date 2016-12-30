import praw


def create_reddit_instance():
    USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 Safari/537.36'
    CLIENT_ID = 'get_your_own_reddit_app_id'
    CLIENT_SECRET = 'get_your_own_reddit_client_secret'
    reddit_instance = praw.Reddit(user_agent=USER_AGENT,
                                  client_id=CLIENT_ID,
                                  client_secret=CLIENT_SECRET)
    return reddit_instance


def collect_posts_for_subreddit(reddit_instance, subreddit_name='conspiracy'):
    for submission in reddit_instance.subreddit(subreddit_name).new():
        print(submission)
    return


reddit_instance = create_reddit_instance()
collect_posts_for_subreddit(reddit_instance)

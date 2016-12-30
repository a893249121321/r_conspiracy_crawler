import praw
import sqlalchemy
from sqlalchemy import MetaData
from sqlalchemy import create_engine


def create_reddit_instance():
    USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 Safari/537.36'
    CLIENT_ID = 'get_your_own'
    CLIENT_SECRET = 'get_your_own'
    reddit_instance = praw.Reddit(user_agent=USER_AGENT,
                                  client_id=CLIENT_ID,
                                  client_secret=CLIENT_SECRET)
    return reddit_instance


class MySQL_Writer:
    def __init__(self):
        self.engine = create_engine('mysql+pymysql://conspiracy:r_conspiracy@localhost/r_conspiracy_data')
        self.metadata = MetaData(self.engine)
        self.job_postings = sqlalchemy.Table('submissions', self.metadata, autoload=True)

    def insert_into_mysql(self, id, author, score, created, title, num_comments, ups, downs):
        command = f"INSERT INTO job_postings VALUES ('{id}', '{author}', '{score}', '{created}', '{title}', '{num_comments}', {ups}, {downs})"
        self.engine.execute(command)


def collect_posts_for_subreddit(mysql_writer, reddit_instance, subreddit_name='conspiracy'):
    for submission in reddit_instance.subreddit(subreddit_name).new():
        mysql_writer.insert_into_mysql(submission.id, submission.author, submission.score,
                                       submission.created, submission.title, submission.num_comments,
                                       submission.ups, submission.downs)
    return


mysql_writer = MySQL_Writer()
reddit_instance = create_reddit_instance()
collect_posts_for_subreddit(mysql_writer, reddit_instance)

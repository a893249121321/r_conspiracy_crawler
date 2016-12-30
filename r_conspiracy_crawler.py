import praw
import pymysql
import sqlalchemy
from pymysql import IntegrityError
from sqlalchemy import MetaData
from sqlalchemy import create_engine
from datetime import datetime, timezone


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
        command = f"INSERT INTO submissions VALUES ('{id}', '{author}', '{score}', '{created}', '{title}', '{num_comments}', {ups}, {downs});"
        try:
            self.engine.execute(command)
        except sqlalchemy.exc.IntegrityError:
            pass # Duplicate found.


def collect_posts_for_subreddit(mysql_writer, reddit_instance, subreddit_name='conspiracy'):
    for submission in reddit_instance.subreddit(subreddit_name).new():
        utc_time = datetime.fromtimestamp(submission.created, timezone.utc)
        local_time = utc_time.astimezone()
        created = local_time.strftime("%Y-%m-%d %H:%M:%S")
        mysql_writer.insert_into_mysql(submission.id,
                                       str(submission.author).encode('latin-1', errors='replace').decode('latin-1'),
                                       submission.score,
                                       created,
                                       submission.title.encode('latin-1', errors='replace').decode('latin-1').replace('\'', '"').replace('%', '%%'),
                                       submission.num_comments,
                                       submission.ups,
                                       submission.downs)
    return


mysql_writer = MySQL_Writer()
reddit_instance = create_reddit_instance()
collect_posts_for_subreddit(mysql_writer, reddit_instance)

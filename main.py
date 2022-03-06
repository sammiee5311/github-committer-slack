from config.database import MongoDB
from typing import List
from committer import Committer
from utils.helper import get_yesterday_commit, post_daily_commits, create_block_message


def main():
    database = MongoDB()
    committers: List[Committer] = []

    for user in database.find_users():
        yesterday_commit = get_yesterday_commit(user['username'])
        committer = Committer(user['username'], user['slack_name'],
                              user['continuous_days'], user['total_commits'], yesterday_commit)
        committers.append(committer)

        if committer.yesterday_commit == 0:
            database.update(committer.username, {"continuous_days": 0})
        else:
            database.update(committer.username, {
                "continuous_days": committer.continuous_days + 1, "total_commits": committer.total_commits + committer.yesterday_commit})

    blocks = create_block_message(committers)
    post_daily_commits(blocks)


if __name__ == '__main__':
    main()

from dataclasses import dataclass


@dataclass
class Committer:
    username: str
    slack_name: str
    continuous_days: str
    total_commits: int
    yesterday_commit: int = 0

import requests
import re
import os
import copy

from slack import WebClient
from committer import Committer
from datetime import datetime, timedelta
from config.env import load_env
from typing import Dict, List, Any

load_env()

OAUTH = os.environ['OAUTH']
CHANNEL = os.environ['CHANNEL']
URI = "https://github.com/users/%s/contributions?to=%s"

DIVIDER = {"type": "divider"}
START_TEXT = {
    "type": "section",
    "text": {"type": "mrkdwn", "text": "[%s] \n\n *총 %d 명 중 %s 명* \n\n 어제 커밋 한 분들입니다."},
}
COMMITERS = {
    "type": "section",
    "text": {
        "type": "mrkdwn",
        "text": "%s %s 님 %s"
    }
}

Blocks = List[Dict[str, Dict[str, str]]]


def get_yesterday_commit(committer: str) -> str:
    yesterday = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
    response = requests.get(URI % (committer, yesterday))
    result = response.content.decode('utf-8')

    yesterday_commit = re.findall(
        f'data-count="([0-9]*)" data-date="{yesterday}"', result)

    return int(yesterday_commit[0]) if len(yesterday_commit) > 0 else 0


def create_block_message(committers: List[Committer]) -> Blocks:
    today = datetime.today().strftime('%Y-%m-%d')
    total = 0
    commits_blocks = [DIVIDER]
    no_commits_blocks = [DIVIDER]

    for committer in committers:
        if committer.yesterday_commit > 0:
            total += 1

        commit_block = copy.deepcopy(COMMITERS)

        if committer.yesterday_commit == 0:
            commit_block['text']['text'] = commit_block['text']['text'] % (
                '', committer.slack_name, '')
            no_commits_blocks.append(commit_block)
        else:
            commit_block['text']['text'] = commit_block['text']['text'] % (
                '🎉', committer.slack_name, f'(연속 {committer.continuous_days + 1} 일 !)')
            commits_blocks.append(commit_block)

    start_block = copy.deepcopy(START_TEXT)
    start_block['text']['text'] = start_block['text']['text'] % (
        today, len(committers), total)

    return [start_block] + commits_blocks + no_commits_blocks


def post_daily_commits(blocks: Blocks):
    client = WebClient(token=OAUTH)

    client.chat_postMessage(
        channel=CHANNEL,
        blocks=blocks)

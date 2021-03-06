# -*- coding:utf-8 -*-
import os
import time
import random
from slackclient import SlackClient


# starterbot's ID as an environment variable
BOT_ID = "U632C7TJT"

# constants
AT_BOT = "<@" + BOT_ID + ">"
HELLO_COMMAND = ["hi", "hello", "하이", "ㅎㅇ", "안녕", "안녕하세요", "안뇽"]
HELLO_RETURN = ["hi", "hello", "하이", "ㅎㅇ", "안녕", "안녕하세요", "안뇽", "ㅇㅇ", "왜?", "OK퀴즈 풀래?", "ㅇㅋ"]
START_TEXT = ["quiz", "game", "게임", "OX", "ox", "퀴즈", "내봐", "문제", "ㅇㅇ"]
OX_ANSWER_O = "O"
OX_ANSWER_X = "X"
GENERAL_POSITIVE_ANSWER_TEXT = ["ㅇ", "ㅇㅇ", "응", "그래", "알았어", "해봐"]
GENERAL_NEGATIVE_ANSWER_TEXT = ["ㄴ", "ㄴㄴ", "그만", "아니", "아니오", "아니요"]

# END_TEXT =

# instantiate Slack & Twilio clients
slack_client = SlackClient('xoxb-207080265639-Ocwc4lEFYUq8QckQKYpVGfIu')

WAIT_ANSWER = False


def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """

    response = "미안해요.. 반나절만에 만든거라 다른 말은 대답 못해요. OX퀴즈나 풀어봅시다!"

    # if WAIT_ANSWER:
    #      #if (check command contains answer text) return 정답여부
    #      #else O나 X로 정답을 입력해주세요
    # else:
    if command in HELLO_COMMAND:
        response = random.choice(HELLO_RETURN)
    elif command in START_TEXT:
        response = "게임을 시작하지.."

        ## 문제 내는 함수

        WAIT_ANSWER = True

    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
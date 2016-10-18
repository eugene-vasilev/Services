import os
import time
from slackclient import SlackClient
import req
import client

# py_compile_bot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")

# constants
AT_BOT = "<@" + BOT_ID + ">"

# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))


def handle_command(command, channel):

    response = """Not sure what you mean. Please use this construction '@py_compile_bot code,lang'/n
                Example: @py_compile_bot print(3+7),9"""

    separated = req.request_conversion(command)
    dict = {1:"C",2:"C++",3:"D",4:"Haskell",5:"Lua",6:"OCaml",7:"PHP",8:"Perl",9:"Python",10:"Ruby",11:"Scheme",12:"Tcl"}

    lang_val=dict[int(separated[1])]
    print lang_val
    bot = client.User()
    response = bot.compile(lang_val,separated[0],True)

    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)


def parse_slack_output(slack_rtm_output):
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip(), \
                       output['channel']
    return None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 0.1 # 0.1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("Py-Compile-Bot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")

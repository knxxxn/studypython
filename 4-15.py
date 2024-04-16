import requests
import json

slack_webhook_url = "https://hooks.slack.com/services/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"

def sendSlackhook(strText):
    headers={
        "Content-type" : "application/json"
    }

    data={
        "text" : strText
    }

    res = requests.post(slack_webhook_url, headers=headers, data=json.dumps(data))

    if res.status_code == 200:
        return "ok"
    else:
        return "error"


print(sendSlackhook("보낼 메세지"))



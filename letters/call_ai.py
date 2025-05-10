from flask import Flask, request, render_template, Response
from http import HTTPStatus
from dashscope import Application
import json

app = Flask(__name__)


@app.route("/")
def home(path=""):
    """
    首页
    """
    return render_template("chat_cat_homepage.html")


def call_with_stream(query):
    """
    流式调用百炼 API
    需要将API Key配置到环境变量
    https://help.aliyun.com/zh/model-studio/developer-reference/configure-api-key-through-environment-variables
    返回数据格式
    id:1
    event:result
    :HTTP_STATUS/200
    data:{"output":{"session_id":"xxx","finish_reason":"null","text":"相关的问题"}}
    """
    # appId 填入百炼应用 ID
    responses = Application.call(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        app_id="011797b6cc2343ff8c9bf5c72cebe978",
        prompt=query,
        stream=True,
        incremental_output=True,
    )
    i = 0
    for response in responses:
        if response.status_code != HTTPStatus.OK:
            print(
                "request_id=%s\n output=%s\n usage=%s\n"
                % (response.request_id, response.output, response.usage)
            )
        else:
            data = (
                "id:"
                + str(i)
                + "\nevent:result\n:HTTP_STATUS/200\ndata:"
                + json.dumps(response)
                + "\n\n"
            )
            yield data


@app.route("/chat", methods=["POST"])
def create():
    raw_data = request.data
    data = json.loads(raw_data.decode("utf-8"))

    return Response(
        call_with_stream(data["prompt"]), mimetype="application/octet-stream"
    )


if __name__ == "__main__":
    app.run(debug=True, port=8080)
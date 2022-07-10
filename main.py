from flask import Flask, request
from os import environ as envv
from vk_api import VkApi, VkUpload
from vk_api.utils import get_random_id

app = Flask(__name__)

@app.route('/',methods=["POST","GET"])
def index():
    pass

@app.route(envv['BOT_ADDRESS'], methods=['POST'])
def bot():
    data = request.get_json(force=True,silent=True)
    if not data or 'type' not in data: return 'not ok'
    if data['secret'] == envv['SECRET']:
        if data['type'] == 'confirmation': return envv['CONFIRMATION_TOKEN']
        elif data['type'] == 'message_new':
            message = data['object']['message']
            if data['object']['message']['from_id'] not in users['items']:
                bs.messages.send(message="Сначала вступи в сообщество",random_id=get_random_id(),user_id=message['from_id'])
                return 'ok'
            else:
                bs.messages.send(message="Красава вступил в сообщество!",random_id=get_random_id(),user_id=message['from_id'])

if __name__ in "__main__":
    botSession = VkApi(token=envv['VK_API_KEY'])
    bs = botSession.get_api()
    users = bs.groups.getMembers(group_id=int(envv['GROUP_ID']))
    app.run(host='0.0.0.0',port=envv['PORT'],debug=True)
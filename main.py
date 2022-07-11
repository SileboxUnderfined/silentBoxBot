from flask import Flask, request
from os import environ as envv
from vk_api import VkApi, VkUpload
from vk_api.utils import get_random_id
import botFuncs

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
            if message['from_id'] not in users['items']: bs.messages.send(message="Сначала вступи в сообщество",random_id=get_random_id(),peer_id=message['from_id'])

            else:
                if message['peer_id'] == message['from_id']:
                    forwarded_messages = message['fwd_messages']
                    if len(forwarded_messages) != 1: bs.messages.send(message='Перешли мне ровно одно(1) сообщение от одного(1) человека!',random_id=get_random_id(),peer_id=message['from_id'])
                    else: botFuncs.createImageCitation(forwarded_messages[0],vupl,bs,message['peer_id'])

                else:
                    if message['text'] == 'хочу кота': botFuncs.createCatImage(vupl,bs,message['peer_id'])

    return 'ok'

if __name__ in "__main__":
    botSession = VkApi(token=envv['VK_API_KEY'])
    bs = botSession.get_api()
    vupl = VkUpload(bs)
    users = bs.groups.getMembers(group_id=int(envv['GROUP_ID']))
    app.run(host='0.0.0.0',port=envv['PORT'],debug=True)
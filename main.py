from flask import Flask, request
from os import environ as envv
from vk_api import VkApi, VkUpload
from vk_api.utils import get_random_id
from io import BytesIO
from imageCitate import ImageCitate
import requests

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
            if message['from_id'] not in users['items']:
                bs.messages.send(message="Сначала вступи в сообщество",random_id=get_random_id(),user_id=message['from_id'])

            else:
                forwarded_messages = message['fwd_messages']
                if len(forwarded_messages) != 1: bs.messages.send(message='Перешли мне ровно одно(1) сообщение от одного(1) человека!',random_id=get_random_id(),user_id=message['from_id'])
                else:
                    forwarded_message = forwarded_messages[0]
                    getAuthor = bs.users.get(user_ids=forwarded_message['from_id'],fields="photo_200")[0]
                    author = getAuthor['first_name'] + getAuthor['last_name']
                    avatar = BytesIO(requests.get(getAuthor['photo_200']).content)
                    text = forwarded_message['text']

                    im = ImageCitate(text=text,creator=author,avatar=avatar)
                    r = im.work()

                    print('test001')

                    buffer = BytesIO()
                    r.save(buffer,'jpeg')
                    buffer.seek(0)

                    print('test002')

                    print(vupl.photo_messages(buffer,message['peer_id']))

    return 'ok'

if __name__ in "__main__":
    botSession = VkApi(token=envv['VK_API_KEY'])
    bs = botSession.get_api()
    vupl = VkUpload(bs)
    users = bs.groups.getMembers(group_id=int(envv['GROUP_ID']))
    app.run(host='0.0.0.0',port=envv['PORT'],debug=True)
from flask import Flask, request
from os import environ as envv
from vk_api import VkApi, VkUpload
import botFuncs
from botFuncs import sendMessage

commands = {
    "catCmds":{
        0:['хочу кота', "хачу ката", "хк","андрей шиза должен умереть в страшных муках","@silentbox1488 хочу кота"]
    },
    "beerCmds":{
        0:['хочу пиво', 'хп', 'хачу пива', 'хачу певка', 'хочу пивка']
    },
    "dogCmds":{
        0:['хочу пса','хочу собаку','хочу артёма','хпс','хачу песеля']
    }
}

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
            if message['from_id'] not in users['items'] and message['from_id'] == message['peer_id']: sendMessage(bs,message="Сначала вступи в сообщество",peer_id=message["from_id"])
            else:
                if message['peer_id'] == message['from_id']:
                    forwarded_messages = message['fwd_messages']
                    if len(forwarded_messages) != 1: sendMessage(bs,"Перешли мне ровно одно(1) сообщение", message["from_id"])
                    else: botFuncs.createImageCitation(forwarded_messages[0],vupl,bs,message['peer_id'])

                else:
                    if message['text'].replace("@silentbox1488,","") in commands['catCmds'][0]: botFuncs.createCatImage(vupl,bs,message['peer_id'])
                    elif message['text'] in commands['beerCmds'][0]: botFuncs.createBeerImage(vupl,bs,message['peer_id'])
                    elif message['text'] in commands['dogCmds'][0]: botFuncs.createDogImage(vupl,bs,message['peer_id'])

    return 'ok'

if __name__ in "__main__":
    botSession = VkApi(token=envv['VK_API_KEY'])
    bs = botSession.get_api()
    vupl = VkUpload(bs)
    users = bs.groups.getMembers(group_id=int(envv['GROUP_ID']))
    app.run(host='0.0.0.0',port=envv['PORT'],debug=True)
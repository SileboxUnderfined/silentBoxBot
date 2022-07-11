from vk_api.utils import get_random_id
from imageCitate import ImageCitate
from io import BytesIO
from os import environ as envv
import requests

def checkAllownessOfMessageUser(bs,user_id,group_id):
    result = bs.messages.isMessagesFromGroupAllowed(user_id=user_id,group_id=group_id)['is_allowed']
    if result == 1: return True
    else: return False

def checkAllownessOfMessagePeer(bs,peer_id,group_id):
    items = bs.messages.getConversationMembers(peer_id=peer_id,group_id=group_id)['items']
    for item in items:
        if str(item['member_id']) == f"-{group_id}": result = item['is_admin']

    return result

def sendMessage(bs,message,peer_id, attach=None):
    if '2000000000' in str(peer_id): allowed = checkAllownessOfMessagePeer(bs,peer_id,envv['GROUP_ID'])
    else: allowed = checkAllownessOfMessageUser(bs,peer_id,envv['GROUP_ID'])
    if not allowed:
        print('невозможно отправить сообщение')
        return

    if attach == None: bs.messages.send(message=message,peer_id=peer_id,random_id=get_random_id())
    else: bs.messages.send(message=message,attachment=attach,peer_id=peer_id,random_id=get_random_id())

def getAttach(owner_id,photo_id):
    return f"photo{owner_id}_{photo_id}"

def createImageCitation(forwarded_message,vupl,bs, peer_id):
    getAuthor = bs.users.get(user_ids=forwarded_message['from_id'], fields="photo_200")[0]
    author = getAuthor['first_name'] + getAuthor['last_name']
    avatar = BytesIO(requests.get(getAuthor['photo_200']).content)
    text = forwarded_message['text']

    im = ImageCitate(text=text, creator=author, avatar=avatar)
    r = im.work()

    buffer = BytesIO()
    r.save(buffer, 'jpeg')
    buffer.seek(0)

    result = vupl.photo_messages(buffer, peer_id)[0]
    attachment = getAttach(result['owner_id'],result['id'])

    sendMessage(bs,message="Готово, держи", attach=attachment, peer_id=peer_id)

def createCatImage(vupl,bs,peer_id):
    jsoned = requests.get("https://api.thecatapi.com/v1/images/search").json()
    catImage = BytesIO(requests.get(jsoned[0]["url"]).content)

    if checkAllownessOfMessagePeer(bs,peer_id,envv['GROUP_ID']):
        result = vupl.photo_messages(catImage)[0]
        attachment = getAttach(result['owner_id'],result['id'])

        sendMessage(bs,message="Держи кота!", peer_id=peer_id, attach=attachment)

    else: print('невозможно загрузить фотографию')
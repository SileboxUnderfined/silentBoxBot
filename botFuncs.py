from vk_api.utils import get_random_id
from imageCitate import ImageCitate
from io import BytesIO
import requests

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

    bs.messages.send(message='Готово, держи', random_id=get_random_id(), user_id=peer_id, attachment=attachment)

def createCatImage(vupl,bs,peer_id):
    jsoned = requests.get("https://api.thecatapi.com/v1/images/search").json()
    catImage = BytesIO(requests.get(jsoned[0]["url"]).content)

    result = vupl.photo_messages(catImage,peer_id)[0]
    attachment = getAttach(result['owner_id'],result['id'])

    bs.messages.send(message="Держи кота!", random_id=get_random_id(), user_id=peer_id, attachment=attachment)
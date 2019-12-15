from datetime import datetime
import requests
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, posts
import pytz


def make_post(title, body, img):
    p = requests.get(img)
    out = open("img.jpg", "wb")
    out.write(p.content)
    out.close()

    client = Client('http://yourdomain.com/xmlrpc.php', 'login', 'password')

    # set to the path to your file
    filename = 'img.jpg'

    # prepare metadata
    data = {
        'name': 'img.jpg',
        'type': 'image/jpeg',
    }
    with open(filename, 'rb') as img:
        data['bits'] = xmlrpc_client.Binary(img.read())

    response = client.call(media.UploadFile(data))
    # response == {
    #       'id': 6,
    #       'file': 'picture.jpg'
    #       'url': 'http://www.yourdomain.com/wp-content/uploads/2012/04/16/picture.jpg',
    #       'type': 'image/jpeg',
    # }
    attachment_id = response['id']

    post = WordPressPost()
    post.title = title #str
    post.content = body #str Text or HTML
    post.id = client.call(posts.NewPost(post))
    post.post_status = 'publish'
    post.thumbnail = attachment_id
    post.terms_names = {
        'post_tag': ['tagA', 'another tag'],
        'category': ['My Category'],
    post.date = datetime.now(pytz.timezone('Etc/GMT+0'))
    client.call(posts.EditPost(post.id, post))


if __name__ == '__main__':
    make_post(title, body, img)

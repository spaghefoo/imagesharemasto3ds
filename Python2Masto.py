from mastodon import Mastodon, MastodonError
import os, filetype

class toMastodon():
    
    def __init__(self, mastodonInstance):
        self.mastoInstance = mastodonInstance
        self.secret_file = 'imgfile3ds'+self.mastoInstance

    
    def initApp(self):
        """
        Create app on the instance if it doesn't exist yet on this instance
        else just creates an instance of the app.
        NEED TO FIND A BETTER WAY TO STORE CREDENTIALS!!!!
        NOT READY FOR MASS PRODUCTION!!!!!!!!!
        """
        if not os.path.exists(self.secret_file):
            Mastodon.create_app(
                'imageshare3ds',
                api_base_url = 'https://'+self.mastoInstance,
                to_file = self.secret_file
            )
        

    def login(self, mail, pwd):
        """
        To login into whatever account, returns the access_token
        """
        mastodon = Mastodon(client_id= self.secret_file)
        access =  mastodon.log_in(
            mail,
            pwd
        )
        return access
    
    def me(self, loginId):   
        mastodon = Mastodon(access_token=loginId, api_base_url='https://'+self.mastoInstance)
        return mastodon.me()
        

    def toot(self, loginId, text, image=None):
        """Takes the access token returned by login(or whatever)
        then takes optioinally an image(path or data)
        and then text(str)
        then posts it to the initially configured mastodon/fediverse instance.
        """
        try:
            mastodon = Mastodon(access_token=loginId, api_base_url=self.mastoInstance)
        except MastodonError as e:
            return e
        else:
            ImgID = None
            if image is not None:
                if os.path.exists(image):
                    if filetype.is_image(image):
                        ImgID = mastodon.media_post(media_file=image, mime_type='image/jpg')
                
            mastodon.status_post(text, media_ids=ImgID)




if __name__ == '__main__':
    Post = toMastodon("blob.cat")
    Post.initApp()
    loginID = Post.login('mastoroma@acheraiou.fr', 'g8Qgo5TtTtf75G6x2n2K')
    Post.toot(loginID, "Spam", '588607.jpg')



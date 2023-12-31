from flask import Flask
from flask import render_template, flash, url_for, request, redirect, session
from werkzeug.utils import secure_filename
import filetype
from Python2Masto import toMastodon
from mastodon import Mastodon, MastodonError, MastodonAPIError, MastodonRatelimitError, MastodonNetworkError, MastodonIllegalArgumentError
from parse3DSTitles import Parse3DSTitles, ParseWiiUTitles, NintendoParseUtils
from PIL import Image, ExifTags
import random, string, os

app = Flask(__name__)
app.secret_key = b'](y(y02d65f'


def toot(loginId, text, mastodoninstance, image=None):
        """Takes the access token returned by login(or whatever)
        then takes optioinally an image(path or data)
        and then text(str)
        then posts it to the initially configured mastodon/fediverse instance.
        """
        try:
            mastodon = Mastodon(access_token=loginId, api_base_url=mastodoninstance)
        except MastodonError as e:
            return e
        else:
            ImgID = None
            if image is not None:
                    if filetype.is_image(image):
                        ImgID = mastodon.media_post(media_file=image, mime_type='image/jpg')
                
            mastodon.status_post(text, media_ids=ImgID)


def InitMasto(instance):
    toMast = toMastodon(instance) 
    toMast.initApp()
    return toMast
    

@app.errorhandler(404)
def notfound(error):
    return render_template('notfound.html.jinja'), 404    
@app.route('/')
def index():
    return render_template('index.html.jinja')

@app.route('/login/masto', methods=['GET', 'POST'])
def login_masto():

    # SI REQUETE POST(tentative de login.)
    if request.method == 'POST':
        try:
            toMast = InitMasto(request.form['instance'])
            session['instance'] = request.form['instance']
            session['token'] = toMast.login(request.form['usr'], request.form['pwd'])
        except MastodonIllegalArgumentError as illegal:
            app.logger.info("ILLEGAL ARGUMENTS REACHED")
            app.logger.warning(illegal)
            flash("Invalid Credientials, please try again")
        except MastodonAPIError as api:
            app.logger.info("API ERROR REACHED")
            app.logger.warning(api)
            flash("Cannot fullfill your request. Please try again later")
        except MastodonNetworkError as net:
            app.logger.info("NETWORK ERROR REACHED")
            app.logger.warning(net)
            flash("Could not contact the instance, check the spelling and try again.")
        except MastodonRatelimitError as rt:
            app.logger.info("RATELIMIT ERROR REACHED")
            app.logger.warning(rt)
            flash("Reached Ratelimit. Please try again in a moment")
        except MastodonError as general:
            app.logger.info("GENERAL ERROR REACHED")
            app.logger.warning(general)
            flash("General Error, try again later")
        else:
            session['usr'] = toMast.me(session['token'])['username']
            return redirect(url_for('post'))
        

    return render_template('login.masto.html.jinja')

    

@app.route('/post', methods=['GET', 'POST'])
def post():
    print(session)
    if 'token' not in session:
        app.logger.info("REDIRECTION VERS LA PAGE D'ACCUEIL CAR PAS CONNECTÉ")
        return redirect(url_for('index'))
    

    if request.method == 'POST':
        img = None
        imgpath = None
        titleName = None
        if request.form['message']:
            tootString = f"{request.form['message']}"
        
        if request.files['img']:
            rand = ''.join(random.choices(string.ascii_uppercase + string.digits, k=7)) #GENERE DES CARACTERES ALÉATOIRES POUR LE STOCKAGE DE L'IMAGE
            img = request.files['img']
            imgpath = f"tmp/{rand}.jpg"
            img.save(imgpath)
            if NintendoParseUtils().is3DSOrWiiU(img):
                # Si c'est une 3DS
                try:
                    softwareId = Parse3DSTitles().getSoftwareId(imgpath)
                    titleName = Parse3DSTitles.returnNameFromTitleID(softwareId).split(' ')
                except ValueError as ve:
                    app.logger.warning(ve)
                    titleName = "Image"
                except TypeError as te:
                    app.logger.warning(te)
                    titleName = "Image"
                else:
                    titleName = ''.join(titleName).lower()
                finally:
                    tootString = f'{request.form['message']} #3DS #{titleName}'
            else:
                # Si c'est une WiiU...
                try:
                    titleName = ParseWiiUTitles().returnNameFromTitleId(secure_filename(img.filename)).split(' ')
                except ValueError as ve:
                    app.logger.warning(ve)
                    titleName = "Image"
                except TypeError as te:
                    app.logger.warning(te)
                    titleName = "Image"
                else:
                    titleName = ''.join(titleName).lower()
                finally:
                    tootString = f'{request.form['message']} #WiiU #{titleName}'

        if 'img' in request.files or 'message' in request.form:
            e = toot(session['token'], tootString, session['instance'] , imgpath)
            os.remove(imgpath)
        else:
            flash("Please post a message")

        if e is not None:
            flash("An error occured during the upload process. please try again later")
        else:
            flash("Message was uploaded successfully!")

   
    return render_template('logon.html.jinja', usr=session['usr'] ,inst=session['instance'])


@app.get('/logoff')
def popoff():
    session.clear()
    flash("You are logged off successfully")
    return redirect(url_for('index'))

@app.get('/about/')
def about():
    return render_template('about.html.jinja')

"""
Tests.
Works on a domain not on ips. fine
@app.get('/test')
def test():
    session['test'] = 'test'
    session.modified = True
    print(session)
    return session['test']

@app.get('/test2')
def test2():
    print(session)
    return session['test']
""" 
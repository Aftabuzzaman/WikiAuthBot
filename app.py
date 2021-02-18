import re, datetime, os, struct
from flask import Flask, request, abort, current_app as app 

from discord_webhook import DiscordWebhook, DiscordEmbed 

discwebhook=open('discweb','r').read()

os.system('clear') 
app = Flask(__name__)
ip_ban_list = ['34.216', '54.189', '54.188', '54.187', '54.186', '54.212', '34.214'] 
big_list = ['34', '54', '35'] 

@app.before_request 
def block_method():
    ip = request.environ.get('REMOTE_ADDR')
    if ip[:2] in big_list:
        print('Ignoring from blacklisted IP')
        abort(403) 

@app.route('/wauth/<discid>/') 
def wauth_oauth(discid):
    if discid == 'favicon.ico':
        return ''
    else:
        try:
            diID = int(discid, 16)
            oauthv = request.args.get('oauth_verifier')
            oautht = request.args.get('oauth_token')
            pas = f'''diID: <@{diID}> {diID}\noauth_verifier: {oauthv}\noauth_token: {oautht}'''
            webhook = DiscordWebhook(url=discwebhook, content=pas, username='WikiOAuthBot')
            response=webhook.execute()
        except:
            return '''<h1>Error</h1> The values provided do not coincide with a successful login, please try again or contact IVORK#0001 on discord.'''
        else:
            return '''<h1>Thanks! Your request has been successfully processed.</h1>You may now close this window as WikiAuthBot should message you back momentarily.<meta http-equiv="refresh" content="2;url=https://meta.wikikimedia.org/wiki/Discord#WikiAuthBot" />'''

@app.route('/mauth/<discid>/') 
def mauth_oauth(discid):
    if discid == 'favicon.ico':
        return ''
    else:
        try:
            diID = int(discid, 16)
            oauthv = request.args.get('oauth_verifier')
            oautht = request.args.get('oauth_token')
            pas = f'''diID: <@{diID}> {diID}\noauth_verifier: {oauthv}\noauth_token: {oautht}'''
            webhook = DiscordWebhook(url=discwebhook, content=pas, username='MikiOAuthBot')
            response=webhook.execute()
        except:
            return '''<h1>Error</h1> The values provided do not coincide with a successful login, please try again or contact IVORK#0001 on discord.'''
        else:
            return '''<h1>Thanks! Your request has been successfully processed.</h1>You may now close this window as WikiAuthBot should message you back momentarily.<meta http-equiv="refresh" content="2;url=https://meta.wikikimedia.org/wiki/Discord#WikiAuthBot" />'''

@app.route('/test/')
def index():
    return 'Hello World!'

if __name__ == '__main__':
    app.run()    

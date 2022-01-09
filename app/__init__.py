import os

from flask import Flask, request

import config
# from .db import db
from .teledisp import init_bot_webhook, init_upd_dispatcher
from .secret import generatekey, generatecsr


def create_app():
    app = Flask(__name__, instance_path=config.Config.CONF_ROOT, instance_relative_config=True)
    key = generatekey(config.Config.CONF_ROOT, config.Config.CERT_KEY)
    cert = generatecsr(key, config.Config.CONF_ROOT, config.Config.CERT, config.Config.HOST_NAME, config.Config.HOST_IP)
    if os.environ.get('FLASK_ENV') == 'development':
        app.config.from_object(config.Development)
    else:
        app.config.from_object(config.Production)
    # db.init_app(app)
    print(app.config['HOST_URL']+app.config['BOT_TOKEN'])
    print(cert)
    try:
        bot, result = init_bot_webhook(app.config['BOT_TOKEN'], app.config['HOST_URL'], app.config['HOST_IP'],
                                       cert)
        if not result:
            raise ValueError
        else:
            disp = init_upd_dispatcher(bot)
    except ValueError:
        print("Webhook is not set!")

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    @app.route('/' + app.config(['BOT_TOKEN']), methods=['POST'])
    def webhook():
        r = request.get_json(force=True, silent=True)
        update = bot.Update.de_json(r, bot)
        disp.process_update(update, app.app_context())
        return "ok", 200

    return app

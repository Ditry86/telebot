from app import create_app
import os
from dotenv import load_dotenv

if __name__ == '__main__':
    app = create_app()
    app.run()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

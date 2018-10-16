import os

from app import app_factory

app = app_factory(os.getenv('ENV'))

if __name__ == '__main__':
    app.run()

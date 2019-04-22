from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask import render_template
from app import create_app
from app.scraper import ScrapeCommand
from app.models import db, UrlIndex
import os

# Environment
env = "development"
if os.getenv('FLASK_ENV') != None:
    env = os.getenv('FLASK_ENV')

# Application
app     = create_app(env, db)
migrate = Migrate(app, db)
manager = Manager(app)

# Management Commands
manager.add_command('database', MigrateCommand)
manager.add_command('scraper', ScrapeCommand)

# Front end demo
@app.route('/')
def demo():
    return render_template('demo.html')

# Away we go...
if __name__ == '__main__':
    manager.run()


from flask_app import app
from flask_app.controllers import login_controller
from flask_app.controllers import show_controller



if __name__ == "__main__":
    app.run(debug=True, port=4200)
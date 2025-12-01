from routes import (
    users, auth, temples, species, masters, padawans,
    lightsabers, crystals, courses, enrollments
)

def register_blueprints(app):
    app.register_blueprint(auth)
    app.register_blueprint(users)
    app.register_blueprint(temples)
    app.register_blueprint(species)
    app.register_blueprint(masters)
    app.register_blueprint(padawans)
    app.register_blueprint(lightsabers)
    app.register_blueprint(crystals)
    app.register_blueprint(courses)
    app.register_blueprint(enrollments)

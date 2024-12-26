from app import create_app, db

# Create the Flask application
app = create_app()

# Ensure application context is available for database operations
with app.app_context():
    db.create_all()  # Create database tables if they don't exist

# Run the application
if __name__ == '__main__':
    app.run(debug=True)

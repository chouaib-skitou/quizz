

# Install the required packages
pip install -r requirements.txt

# Make migrations
python manage.py makemigrations

# Apply the migrations
python manage.py migrate

# Run the server
python manage.py runserver
https://superset.incubator.apache.org/installation.html#superset-installation-and-initialization

	# Install superset
	pip install superset

	# Create an admin user (you will be prompted to set username, first and last name before setting a password)
	fabmanager create-admin --app superset

	# Initialize the database
	superset db upgrade

	# Load some data to play with
	superset load_examples

	# Create default roles and permissions
	superset init

	# To start a development web server on port 8088, use -p to bind to another port
	superset runserver -d

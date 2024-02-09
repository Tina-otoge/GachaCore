from .models import db
from .parser import main

# db.drop_database()
db.create_database()

main()

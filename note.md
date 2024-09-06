# Create virtual env
py -3 -m venv <name>
pip freeze > requirements.txt
pip install -r  requirements.txt
alx-venv/Scripts/activate
 git rm -r --cached
flask --app app.app run --debug
find backend -type f -path "*activate*"
 export PATH=$PATH:$(pwd)/backend/alx-venv/Scripts/activate
git rm -r --cached ./**/*__pyca*
``
 alias py=$(pwd)/backend/alx-venv/Scripts/python.exe
export PATH = $PATH:"/c/Users/Adeyori/alx-project/backend/alx-venv/Scripts/"

export PATH=$PATH:"/c/Users/Adeyori/alx-project/backend/alx-venv/Scripts/" (for bash in window os)
export PATH=$(cat path.txt):/c/Users/Adeyori/alx-project/backend/alx-venv/Scripts/
/c/Users/Adeyori/alx-project/backend/alx-venv/Scripts/pip install Flask (bash term in window os)
/c/Users/Adeyori/alx-project/backend/alx-venv/Scripts/pip install -U flask-cors
/c/Users/Adeyori/alx-project/backend/alx-venv/Scripts/pip install install mypy

/c/Users/Adeyori/alx-project/backend/alx-venv/Scripts/pip freeze > requirements.txt
pip freeze > requirements.txt
/c/Users/Adeyori/alx-project/backend/alx-venv/Scripts/mypy
/c/Users/Adeyori/alx-project/backend/alx-venv/Scripts/pip install flasgger

pip install --pre SQLAlchemy
pip install python-dotenv
 pip install mysqlclient
 pip install bcrypt

pip install PyMySQL 

Flask uses a concept of blueprints for making application components

```
from sqlalchemy import create_engine
engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
with engine.connect() as conn:
...     result = conn.execute(text("select 'hello world'"))
...     print(result.all())


with engine.connect() as conn:
    conn.execute(text("CREATE TABLE some_table (x int, y int)"))
    conn.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": 1, "y": 1}, {"x": 2, "y": 4}],
    )
    conn.commit()


    with engine.begin() as conn:
    conn.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": 6, "y": 8}, {"x": 9, "y": 10}],
    )

    Using session

 from sqlalchemy.orm import Session

stmt = text("SELECT x, y FROM some_table WHERE y > :y ORDER BY x, y")
with Session(engine) as session:
    result = session.execute(stmt, {"y": 6})
    for row in result:
        print(f"x: {row.x}  y: {row.y}")

        .execute
        .get_all
        .get
        .update
        


===============================================
 database metadata in SQLAlchemy are known as MetaData, Table, and Column

 from sqlalchemy import MetaData
 from sqlalchemy import Table, Column, Integer, String
 metadata_obj = MetaData()
user_table = Table(
    "user_account",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(30)),
    Column("fullname", String),
)

user_table.c.name

user_table.c.keys()
```

# write two table user and address where user has many addresses and  addresses point to one user

```
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from base_model import  # Assuming these are defined elsewhere
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    """Representation of a user"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False, unique=True)
    
    # One-to-many relationship with Address
    addresses = relationship("Address", backref="user", cascade="all, delete, delete-orphan")

class Address( Base):
    """Representation of an address"""
    __tablename__ = 'addresses'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    street = Column(String(128), nullable=False)
    city = Column(String(128), nullable=False)
    state = Column(String(128), nullable=False)
    zip_code = Column(String(20), nullable=False)


```


```
creating db connection

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

engine = create_engine('sqlite:///yourdatabase.db')  # Change this to your actual database URL
Base.metadata.bind = engine
Base.metadata.create_all(engine)
db_session = scoped_session(sessionmaker(bind=engine))

```


```
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from base_model import BaseModel, Base  # Assuming these are defined elsewhere

class User(BaseModel, Base):
    """Representation of a user"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False, unique=True)
    
    # One-to-one relationship with Profile
    profile = relationship("Profile", uselist=False, back_populates="user")

class Profile(BaseModel, Base):
    """Representation of a user profile"""
    __tablename__ = 'profiles'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    bio = Column(String(256))
    address = Column(String(128))
    
    # One-to-one relationship with User
    user = relationship("User", back_populates="profile")
```





# To clarify the differences between one-to-one and one-to-many relationships in SQLAlchemy, let's consider examples of both types of relationships, including how to set them up and the underlying database schema.

### One-to-One Relationship

A one-to-one relationship means that each row in one table is linked to exactly one row in another table and vice versa. For instance, each `User` has one `Profile`, and each `Profile` belongs to one `User`.

#### Example: One-to-One Relationship

#### Models

```python
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from base_model import BaseModel, Base  # Assuming these are defined elsewhere

class User(BaseModel, Base):
    """Representation of a user"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False, unique=True)
    
    # One-to-one relationship with Profile (with useLisT=FALSE)
    profile = relationship("Profile", uselist=False, back_populates="user")

class Profile(BaseModel, Base):
    """Representation of a user profile"""
    __tablename__ = 'profiles'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    bio = Column(String(256))
    address = Column(String(128))
    
    # One-to-one relationship with User
    user = relationship("User", back_populates="profile")
```

#### Database Schema

- `users` table:
  - `id`: Primary key.
  - `name`: User's name.
  - `email`: User's email.
  
- `profiles` table:
  - `id`: Primary key.
  - `user_id`: Foreign key referencing `users.id`.
  - `bio`: User's bio.
  - `address`: User's address.

### One-to-Many Relationship

A one-to-many relationship means that each row in one table is linked to multiple rows in another table. For instance, a `User` can have multiple `Address` entries, but each `Address` belongs to one `User`.

#### Example: One-to-Many Relationship

#### Models

```python
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from base_model import BaseModel, Base  # Assuming these are defined elsewhere

class User(BaseModel, Base):
    """Representation of a user"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False, unique=True)
    
    # One-to-many relationship with Address
    addresses = relationship("Address", backref="user", cascade="all, delete, delete-orphan")

class Address(BaseModel, Base):
    """Representation of an address"""
    __tablename__ = 'addresses'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    street = Column(String(128), nullable=False)
    city = Column(String(128), nullable=False)
    state = Column(String(128), nullable=False)
    zip_code = Column(String(20), nullable=False)
```

#### Database Schema

- `users` table:
  - `id`: Primary key.
  - `name`: User's name.
  - `email`: User's email.
  
- `addresses` table:
  - `id`: Primary key.
  - `user_id`: Foreign key referencing `users.id`.
  - `street`: Address street.
  - `city`: Address city.
  - `state`: Address state.
  - `zip_code`: Address zip code.

### Key Differences

1. **Cardinality**:
   - **One-to-One**: Each entity in Table A is related to exactly one entity in Table B and vice versa.
   - **One-to-Many**: Each entity in Table A is related to multiple entities in Table B, but each entity in Table B is related to exactly one entity in Table A.

2. **SQLAlchemy Relationship Configuration**:
   - **One-to-One**: Use `uselist=False` in the `relationship` to indicate the relationship is one-to-one.
   - **One-to-Many**: The default behavior of `relationship` supports one-to-many, so you don't need to set `uselist`.

3. **Database Schema**:
   - **One-to-One**: Each table has a primary key, and one of the tables has a foreign key that is also unique (often acting as its primary key or another unique key).
   - **One-to-Many**: The child table (the "many" side) has a foreign key that references the primary key of the parent table (the "one" side).

### Summary

In a one-to-one relationship, each record in one table corresponds to exactly one record in another table, while in a one-to-many relationship, a single record in one table can correspond to multiple records in another table. SQLAlchemy handles these relationships with the `relationship` function, and the schema design reflects the nature of the relationships with foreign keys and, in the case of one-to-one, unique constraints.


# Repair Previ Table
The error message "#1034 - Index for table 'global_priv' is corrupt; try to repair it" indicates that there is a corruption in the index of the `global_priv` table in the MySQL `mysql` database, which stores user privileges and other metadata. This is a critical issue because it can affect the security and functionality of your MySQL server.

Here's how you can attempt to repair the corrupted table:

### Steps to Repair the Corrupted Table

1. **Stop the MySQL Service**:
    - Open the XAMPP Control Panel.
    - Stop the MySQL service.

2. **Backup Your Data**:
    - Before making any changes, it's crucial to back up your MySQL data directory.
    - Navigate to the `xampp/mysql/data` directory and copy the entire `data` folder to a safe location.

3. **Start MySQL in Safe Mode**:
    - Open a command prompt (CMD) or terminal.
    - Navigate to the `xampp/mysql/bin` directory.
    - Start MySQL with the `--skip-grant-tables` option to bypass the privilege system:

    ```sh
    mysqld --skip-grant-tables --skip-networking
    ```

    - Leave this terminal open as MySQL will run in safe mode here.

4. **Open Another Command Prompt or Terminal**:
    - Navigate to the `xampp/mysql/bin` directory.
    - Open the MySQL command line tool:

    ```sh
    mysql
    ```

5. **Repair the Corrupted Table**:
    - Once in the MySQL command line tool, select the `mysql` database:

    ```sql
    USE mysql;
    ```

    - Attempt to repair the `global_priv` table:

    ```sql
    REPAIR TABLE global_priv;
    ```

6. **Check and Optimize the Table**:
    - After repairing, it's good practice to check and optimize the table:

    ```sql
    CHECK TABLE global_priv;
    OPTIMIZE TABLE global_priv;
    ```

7. **Restart MySQL Normally**:
    - Stop MySQL running in safe mode by closing the terminal where you started it.
    - Start the MySQL service normally through the XAMPP Control Panel.

### Additional Steps if Repair Fails

If the above steps don't resolve the issue, you might need to manually restore the `global_priv` table:

1. **Restore from Backup**:
    - If you have a recent backup of your `mysql` database, restore the `global_priv` table from that backup.

2. **Recreate the Table**:
    - As a last resort, you can recreate the `global_priv` table. This involves significant risk and you may lose user privilege data, so proceed with caution.
    - You can find the schema for the `global_priv` table in the MySQL documentation or from another MySQL installation with the same version.

### Example: Recreating the `global_priv` Table

If you decide to recreate the table, here is an example schema from MySQL 8.0:

```sql
DROP TABLE IF EXISTS `global_priv`;
CREATE TABLE `global_priv` (
  `Host` char(255) COLLATE utf8mb4_bin NOT NULL DEFAULT '',
  `User` char(32) COLLATE utf8mb4_bin NOT NULL DEFAULT '',
  `Priv` json NOT NULL,
  `plugin` char(64) COLLATE utf8mb4_bin DEFAULT 'mysql_native_password',
  `authentication_string` text COLLATE utf8mb4_bin,
  `password_last_changed` timestamp NULL DEFAULT NULL,
  `password_lifetime` smallint unsigned DEFAULT NULL,
  `account_locked` enum('N','Y') COLLATE utf8mb4_bin NOT NULL DEFAULT 'N',
  PRIMARY KEY (`Host`,`User`),
  KEY `User` (`User`),
  KEY `Host` (`Host`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin STATS_PERSISTENT=0 COMMENT='Global privileges';
```

Please ensure you understand the implications of recreating the table and restoring user privileges.

By following these steps, you should be able to repair the corrupted `global_priv` table in your MySQL database running on XAMPP. 



```
CREATE TABLE users (
    id INTEGER NOT NULL AUTO_INCREMENT,
    user_id VARCHAR(60) NOT NULL,
    first_name VARCHAR(60) NOT NULL,
    profile_pix VARCHAR(120) NOT NULL,
    middle_name VARCHAR(60) NOT NULL,
    last_name VARCHAR(60) NOT NULL,
    email VARCHAR(225) NOT NULL,
    password VARBINARY(64) NOT NULL,  -- Changed to VARBINARY
    password2 TINYBLOB(64) NOT NULL,  -- Changed to VARBINARY
    gender VARCHAR(15) NOT NULL,
    date_of_birth DATETIME NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (user_id)
);

CREATE TABLE addresses (
    id INTEGER NOT NULL AUTO_INCREMENT,
    user_id VARCHAR(60) NOT NULL,
    street VARCHAR(128) NOT NULL,
    city VARCHAR(128) NOT NULL,
    state VARCHAR(128) NOT NULL,
    zip_code VARCHAR(20) NOT NULL,
    created_at DATETIME,
    updated_at DATETIME,
    PRIMARY KEY (id),
    FOREIGN KEY(user_id) REFERENCES users(user_id)
);


```


 # file = request.files.get('file')
        file = args['file']
        #Users.add_all()
        # upload(jsonify, file)
        # Handle file saving if a file is uploaded
        # if file:
        #     file_path = f'{root_folder}upload\\{file.filename}'
        #     file.save(file_path)
       

# Structure, response framing 
The `@marshal_with` decorator in Flask-RESTful is used to format the response output of a resource method. It ensures that the returned data is serialized according to a specified structure. This is particularly useful for enforcing consistency and for easily converting complex objects into JSON or other formats.

Here's a basic example to illustrate how `@marshal_with` works in Flask-RESTful:

1. **Install Flask-RESTful**:
   Make sure you have Flask-RESTful installed. If not, you can install it using pip:
   ```bash
   pip install flask-restful
   ```

2. **Define the resource fields**:
   You need to define the structure of the response using `fields` from Flask-RESTful. This can include specifying the types of each field in the response.

3. **Create the resource and use `@marshal_with`**:
   Apply the `@marshal_with` decorator to your resource methods.

Here's an example:

```python
from flask import Flask
from flask_restful import Api, Resource, fields, marshal_with

app = Flask(__name__)
api = Api(app)

# Define the response structure
resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'age': fields.Integer,
    'email': fields.String,
}

# Create a mock database
users = [
    {'id': 1, 'name': 'John Doe', 'age': 30, 'email': 'john@example.com'},
    {'id': 2, 'name': 'Jane Doe', 'age': 25, 'email': 'jane@example.com'},
]

class UserResource(Resource):
    @marshal_with(resource_fields)
    def get(self, user_id):
        user = next((user for user in users if user['id'] == user_id), None)
        if not user:
            return {'message': 'User not found'}, 404
        return user

api.add_resource(UserResource, '/users/<int:user_id>')

if __name__ == '__main__':
    app.run(debug=True)
```

### Explanation

1. **Define `resource_fields`**:
   This dictionary defines the expected structure and types of the fields in the response. Here, each user has an `id`, `name`, `age`, and `email`.

2. **Create a mock database**:
   For this example, `users` is a list of dictionaries representing user data.

3. **Create the `UserResource` class**:
   - The `@marshal_with(resource_fields)` decorator is applied to the `get` method. This ensures that the returned user data will be serialized according to the structure defined in `resource_fields`.
   - The `get` method searches for a user by `user_id`. If the user is found, it is returned. If not, a 404 error message is returned.

4. **Add the resource to the API**:
   The `UserResource` is added to the API with the endpoint `/users/<int:user_id>`.

When you run this application and make a GET request to `/users/1`, it will return the user data formatted as specified in `resource_fields`. If the user with the specified `user_id` does not exist, it will return a 404 error with a message indicating that the user was not found.
  

root password reset for mysql
- mysqladmin --user=root password "root"
-  C:\xampp\mysql\bin\mysqld --init-file=mysql-init.txt

Plugin 'FEEDBACK' is disabled.
 cpoy all from myql folder in data

 (MySQLdb.OperationalError) (1813, "Tablespace for table '`dbname`.`tablename`' exists. Please DISCARD the tablespace before IMPORT")

 go into your data folder, delete the content of folder or the db folder

 pytest --collect-only

 pip install python-dotenv pytest-dotenv  for pytest to detect env variable


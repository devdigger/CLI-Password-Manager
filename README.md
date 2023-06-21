# Password Manager README

This code represents a simple password manager application implemented in Python. It allows users to store and manage passwords for different websites or services in an encrypted database.

## Prerequisites
- Python 3.x
- Required Python libraries: bcrypt, sqlite3, traceback, cryptography

## Setup
1. Ensure you have Python 3.x installed on your system.
2. Install the required Python libraries by running the following command:

```
pip install bcrypt sqlite3 cryptography
```
3. Download or copy the code into a Python file (e.g., `password_manager.py`).

## Usage
1. Run the Python script:
```
python password_manager.py
```
2. If the database file (`test.db`) doesn't exist, the script will create it automatically.
3. If a master password is not set, you will be prompted to enter a new master password. This password will be used to encrypt and decrypt your stored passwords.
4. Once the master password is set or if it already exists, you can start using the password manager with the following options:
- **Display all records** - Displays all stored passwords in the database.
- **View Record** - Retrieves and displays the details of a specific password record by providing its ID.
- **Search Records** - Searches for and displays password records that match a given site name.
- **Add New Record** - Adds a new password record to the database, prompting you to enter the site name, username, and password.
- **Delete Record** - Deletes a password record from the database by providing its ID.
- **Exit** - Exits the password manager application.

Note: All passwords are encrypted using the master password before being stored in the database.

## Security
- The master password is hashed using bcrypt and stored in the database. It is used to verify the correctness of the entered master password.
- Passwords for individual sites are encrypted using the Fernet symmetric encryption algorithm from the cryptography library. The master password is used as the encryption key.

## Database
The password manager uses an SQLite database (`test.db`) to store password records. The database contains a single table called `PASSWORDS` with the following schema:
```
CREATE TABLE PASSWORDS (
ID INT PRIMARY KEY NOT NULL,
SITE TEXT NOT NULL,
USERNAME TEXT NOT NULL,
PASSWORD TEXT NOT NULL
);
```
The table has four columns:
- `ID`: An integer representing the record's unique identifier.
- `SITE`: The name of the website or service associated with the password.
- `USERNAME`: The username or account name for the site.
- `PASSWORD`: The encrypted password for the site.

## Disclaimer
This password manager code is provided as a demonstration and should not be used for storing sensitive or critical passwords without further security enhancements. It's recommended to use dedicated password management tools that have undergone thorough security reviews and offer additional features like secure password generation, multi-factor authentication, and data backups.

Use this code at your own risk. The developers and contributors to this project are not liable for any loss or damage caused by the use of this code.

## License
This code is provided under the [MIT License](https://opensource.org/licenses/MIT).

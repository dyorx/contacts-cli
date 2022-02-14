# Simple Contacts CLI

## Usage:
```bash
$ python contacts.py init # creates a db.json file if not exist

$ python contacts.py add first_name=Pabitra last_name=Shrestha sex=Female address=Kathmandu, Nepal # adds a new contact

$ python contacts.py get id=1 # retrieves the contact by id or any attribute

$ python contacts.py update 1 address=Michigan, USA # updates the address for given id, Note: 1st argument is id, followed by keyword arguments

$ python contacts.py remove 1 # removes the contact with id 1

$ python contacts.py search Pabitra # searches the contacts database by first name
```

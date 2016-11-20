# Mail CR
Automatically send CR emails given URLs.

## Requirements
- Python 3
- Jinja 2

## Config
You need to create a `config.py` file in `src/mailer`. The file should define the following constants :

```python
SENDER = 'your@email.com'
USERNAME = 'username@email.com'
DEST_BURO = 'buro@email.com'
DEST_CA = 'ca@email.com'
PWD = 'yourS3cr3tp4ssw0rd'
SERVER = 'smtp.email.com'
PORT = 4242
TLS = True/False
```


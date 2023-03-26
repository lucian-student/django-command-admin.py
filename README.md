[![](https://img.shields.io/badge/released-2021.6.10-green.svg?longCache=True)](https://pypi.org/project/django-admin-commands/)
[![](https://img.shields.io/badge/license-Unlicense-blue.svg?longCache=True)](https://unlicense.org/)

### Description 

This project is fork of [django_admin_commands](https://github.com/andrewp-as-is/django-command-admin.py).

### Display command

settings
```python
# prefix of displayed commands
DJANGO_ADMIN_COMMANDS_PREFIX="run"
DJANGO_ADMIN_COMMANDS_ALLOW_DELETE = True
DJANGO_ADMIN_COMMANDS_ALLOW_EDIT = True
DJANGO_ADMIN_COMMANDS_ALLOW_ADD = True
# synchronizes commands filtered
DJANGO_ADMIN_COMMANDS_SYNC = True
```

### Installation
```bash
$ pip install django-command-admin
```

#### `settings.py`
```python
INSTALLED_APPS+=['django_admin_commands']
```

#### `migrate`
```bash
$ python manage.py migrate
```


# smdib
Revert of smdib.

# How to run
* Create a credential.json file in workspace root directory. And put username and password in it. For example,
```
{
    "username":"admin",
    "password":"123456"
}
```
* Run main.py

# Call from outer module
```python
# -*- coding: utf-8 -*-

from bidms import bidms


def hello():
    b = bidms.Bidms("administrator", 'password')
    # data = b.get_tong_feng_kong_tiao()
    # for d in data:
    #     print d
    data = b.get_electric_meter()
    for d in data:
        print d

```

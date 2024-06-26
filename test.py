username, password = None, None
if username is not None and password is not None:
    access_token, refresh_token = 1, 2
else:
    access_token, refresh_token = None, None
print(access_token, refresh_token)
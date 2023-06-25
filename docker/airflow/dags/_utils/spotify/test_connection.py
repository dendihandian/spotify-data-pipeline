from _utils.spotify.client import refresh_access_token

def refresh_token():
    return refresh_access_token()

if __name__ == '__main__':
    print(refresh_token())

import uuid
import hmac
import hashlib
import base64


def generateToken(appSecret: "str", duuid=None) -> "str":
    '''
    Return api key , with user provided secret and optiona; uuid

    :param appSecret The secret key used with hmac
    :param duuid: optional user provided uuid hex value

    '''

    duuid = duuid if duuid else uuid.uuid4().hex
    key = hmac.new(
        appSecret.encode(),
        duuid.encode(),
        hashlib.sha256
    ).hexdigest()+" "+duuid

    api_key = base64.urlsafe_b64encode(key.encode()).decode()

    return api_key, duuid


def verify_token(key: "str", appSecret: "str") -> "bool":
    '''
    Get key and verify 
    Returns true if token is verified
    '''
    dKey = base64.urlsafe_b64decode(key.encode()).decode()
    user_digest, duuid = dKey.split()

    if duuid == None:
        return False

    computed_digest = hmac.new(appSecret.encode(),
                               duuid.encode(),
                               hashlib.sha256
                               ).hexdigest()

    return hmac.compare_digest(user_digest.encode(), computed_digest.encode()), duuid


if __name__ == "__main__":
    secret = "123"
    gt = generateToken(secret)
    print(verify_token(gt, secret))

from database.models import Purchasers
from utils.data import *
from string import digits, ascii_letters
from random import choice
from sklearn.metrics.pairwise import cosine_similarity
from numpy import array

def get_rand_str():
    return ''.join(choice(ascii_letters) for i in range(25))

def get_rand_phone():
    return '7' + ''.join(choice(digits) for i in range(10))

async def register(fdesc, namehash, name, phone_number, payment_token):
    try:
        fdesc = decode_vec(fdesc)
        purchaser = await Purchasers.query.order_by(Purchasers.fdesc.cosine_distance(fdesc)).gino.first()
        if purchaser is not None:
            d = cosine_similarity(array(fdesc).reshape(1, -1), array(purchaser.fdesc).reshape(1, -1))[0][0]
        else:
            d = 0

        if d < 0.90:
            print(d)
            purchaser = await Purchasers.create(
                fdesc=fdesc,
                namehash=namehash,
                name=name,
                phone_number=phone_number,
                payment_token=payment_token
            )
            print('registered', purchaser.name)
            #print('registered', purchaser.fdesc)
            return 0
        else:
            print(f'already in db: {purchaser.name}, distance: {d}')
            return 1


    except Exception as e:
        print(e)
        print(e.__repr__())
        return False


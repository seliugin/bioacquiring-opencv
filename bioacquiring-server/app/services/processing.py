from database.models import Purchasers
from third.sbp import SbpAPI
from third.biort import BioAPI
from utils.data import decode_vec
from sklearn.metrics.pairwise import cosine_similarity
from numpy import array

async def process(fdesc):
    try:
        fdesc = decode_vec(fdesc)
        purchaser = await Purchasers.query.order_by(Purchasers.fdesc.cosine_distance(fdesc)).gino.first()

        if purchaser is not None:
            d = cosine_similarity(array(fdesc).reshape(1, -1), array(purchaser.fdesc).reshape(1, -1))[0][0]
        else:
            d = 0

        if d > 0.9:
            print(f'processed ({purchaser.name}) {d}')
            if BioAPI.confirm(fdesc, purchaser.namehash) and SbpAPI.process(purchaser.payment_token, purchaser.phone_number):
                return purchaser.name
        else:
            print(f'not processed ({purchaser.name}) {d}')
            return False

    except Exception as e:
        print(e)
        print(e.__repr__())
        return False



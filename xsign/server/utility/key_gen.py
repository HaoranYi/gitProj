from Crypto.PublicKey import RSA
from Crypto import Random


def generate(pub_key_fn, prv_key_fn, fmt, l):
    random_generator = Random.new().read
    key = RSA.generate(l, random_generator)

    pub_key=key.publickey().exportKey(fmt)
    prv_key=key.exportKey(fmt)

    print('public key:')
    print(pub_key)
    print()
    print('privatekey:')
    print(prv_key)

    if pub_key_fn:
        with open(pub_key_fn, 'wb') as f:
            f.write(pub_key)

    if prv_key_fn:    
        with open(prv_key_fn, 'wb') as f:
            f.write(prv_key)

if __name__ == '__main__':
    from argparse import ArgumentParser
    
    parser = ArgumentParser()
    parser.add_argument('-f', '--format', default='PEM', type=str, 
            help='format for the keys (default: %(default)s)')
    parser.add_argument('-l', '--length', default=1024, type=int, 
            help='key length (default: %(default)s)')
    parser.add_argument('--pubkeyfile', default='public.pem', type=str, 
            help='public key file (default: %(default)s)')
    parser.add_argument('--prvkeyfile', default='private.pem', type=str, 
            help='private key file (default: %(default)s)')
    
    args = parser.parse_args()
    fmt = args.format 
    l = args.length
    pub_key_fn = args.pubkeyfile
    prv_key_fn = args.prvkeyfile

    generate(pub_key_fn, prv_key_fn, fmt, l)



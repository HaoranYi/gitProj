from Crypto.PublicKey import RSA

def test(pub_key_fn, prv_key_fn):
    m = b'abcdefg'
    print(m)

    with open(prv_key_fn, 'rb') as f:
        prv_key = RSA.importKey(f.read())

    with open(pub_key_fn, 'rb') as f:
        pub_key = RSA.importKey(f.read())

    m1 = pub_key.encrypt(m, 32)
    m2 = prv_key.decrypt(m1)
    print()
    print(m1)
    print()
    print(m2)


if __name__ == '__main__':
    from argparse import ArgumentParser
    
    parser = ArgumentParser()
    parser.add_argument('--pubkeyfile', default='public.pem', type=str, 
            help='public key file (default: %(default)s)')
    parser.add_argument('--prvkeyfile', default='private.pem', type=str, 
            help='private key file (default: %(default)s)')
    
    args = parser.parse_args()
    pub_key_fn = args.pubkeyfile
    prv_key_fn = args.prvkeyfile

    test(pub_key_fn, prv_key_fn)



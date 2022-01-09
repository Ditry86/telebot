from OpenSSL import crypto
import os
import whois


def generatekey(ap_path, key_name):

    key = crypto.PKey()
    keypath = os.path.join(ap_path, key_name)
    key.generate_key(crypto.TYPE_RSA, 2048)
    print(crypto.dump_privatekey(crypto.FILETYPE_PEM, key))
    f = open(keypath, "wb")
    f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key))
    f.close()
    return key


def generatecsr(key, ap_path, cert_name, fqdn, ip):

    certpath = os.path.join(ap_path, cert_name)
    cert = crypto.X509()
    w=whois.whois(fqdn)

    if not w.get('country'):
        if not fqdn: cn = ip
        else: cn = fqdn
        c = 'RU'
        st = 'Amur'
        l = 'Blag'
        o = 'Self'
    else:
        c = str(w.get('country'))
        st = str(w.get('state')).lower().title()
        l = str(w.get('city')).lower().title()
        o = str(w.get('org')).lower().title()

    cert.get_subject().CN = fqdn
    cert.get_subject().C = c
    cert.get_subject().ST = st
    cert.get_subject().L = l
    cert.get_subject().O = o
    cert.set_serial_number(1000)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(315360000)
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(key)
    cert.sign(key, 'sha256')

    f = open(certpath, "wb")
    f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
    f.close()
    return certpath


import zlib
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


private_key = "##Private key goes here##"
rsakey = RSA.importKey(private_key)
rsakey = PKCS1_OAEP.new(rsakey)
chunk_size = 256
offset = 0 
decrypted = ""

encrypted = base64.b64decode(encrypted)

while offset < len(encrypted):
	decrypted += rsakey.decrypt(encrypted[offset:offset+chunk_size])
	offset += chunk_size
	#Decompress original

	plaintext = zlib.decompress(decrypted)
print plaintext

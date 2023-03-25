head1 = b'\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
payload1 = b'\xaa'
eop = (1).to_bytes(3,byteorder='big')

handshake = (head1+payload1+eop)

print(handshake)



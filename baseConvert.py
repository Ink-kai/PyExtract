# 十六进制转bytes
import binascii


def hex_to_bytes(hex):
    return bytes.fromhex(hex)
# bytes转十六进制
def bytes_to_hex(bytes):
    return binascii.unhexlify(bytes)
# bytes转字符串
def bytes_to_str(bytes):
    return str(bytes, encoding = "utf-8")
if __name__ == '__main__':
    print(hex_to_bytes("6f"))
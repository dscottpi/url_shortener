base62 = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
base = 62

def encode(n: int): 
    if n == 0:
        return base62[0]

    remainder: int = 0
    encoded_string: list = []
    encoded_string_append = encoded_string.append

    while n > 0:
        remainder = n % base
        n = n // base
        
        encoded_string_append(base62[remainder])
    
    encoded_string.reverse()
    
    return ''.join(encoded_string)

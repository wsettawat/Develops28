

#z1 = str((hex(int(-2)).format(13))
z2=hex(21)
#z3=round(z2,4)
#print(z2)
#https://www.reddit.com/r/learnpython/comments/psdwe3/decimal_to_hex_signed_2s_complement/
a=21
b=205

def tohex(val, nbits):
  return hex((val + (1 << nbits)) % (1 << nbits))

print (tohex(199703103, 64))


if(b==0):
    print("zero")
    p=(tohex(b, 8))
    y=(p.replace('0x', '000'))
    print(y)


elif(b>=0):
    print("positive")
    p=(tohex(b, 8))
    y=(p.replace('0x', '00'))
    print(y)
    
elif(b<0):
    print("negative")
    n=(tohex(b, 8))
    z=(n.replace('0x', 'ff'))
    print(z)
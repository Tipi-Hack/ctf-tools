# Very simple TCP client for a remote interactive service
# Using pwntools https://docs.pwntools.com/en/stable/

from pwnlib.tubes.remote import remote

print "Connecting"
r = remote('hostname', 10001)
r.recvuntil("Choice? ")
print "Send 2"
r.sendline("2")
r.recvuntil("Url? ")
print "Send url"
r.sendline('http://url')
print "-> "
r.interactive()

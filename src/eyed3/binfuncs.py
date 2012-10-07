################################################################################
#  Copyright (C) 2001  Ryan Finne <ryan@finnie.org>
#  Copyright (C) 2002-2011  Travis Shirk <travis@pobox.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
################################################################################


##
# Accepts a string of bytes (chars) and returns an array of bits
# representing the bytes in big endian byte order.
#
# \param bytes String of characters to convert.
# \param sz An optional max size for each byte (default 8 bits/byte) which can
#           be used to mask out higher bits.
def bytes2bin(bytes, sz=8):
    if sz < 1 or sz > 8:
       raise ValueError("Invalid sz value: %d" % sz)

    '''
    # I was willing to bet this implementation was gonna be faster, tis not
    retval = []
    for bite in bytes:
        bits = [int(b) for b in bin(ord(bite))[2:].zfill(8)][-sz:]
        assert(len(bits) == sz)
        retval.extend(bits)
    return retval
    '''

    retVal = []
    for b in bytes:
        bits = []
        b = ord(b)
        while b > 0:
            bits.append(b & 1)
            b >>= 1

        if len(bits) < sz:
            bits.extend([0] * (sz - len(bits)))
        elif len(bits) > sz:
            bits = bits[:sz]

        # Big endian byte order.
        bits.reverse()
        retVal.extend(bits)

    return retVal


## Convert an array of bits (MSB first) into a string of characters.
def bin2bytes(x):
    bits = []
    bits.extend(x)
    bits.reverse()

    i = 0
    out = ''
    multi = 1
    ttl = 0
    for b in bits:
        i += 1
        ttl += b * multi
        multi *= 2
        if i == 8:
            i = 0
            out += chr(ttl)
            multi = 1
            ttl = 0

    if multi > 1:
        out += chr(ttl)

    out = list(out)
    out.reverse()
    out = ''.join(out)
    return out


## Convert and array of "bits" (MSB first) to it's decimal value.
def bin2dec(x):
    bits = []
    bits.extend(x)
    bits.reverse()  # MSB

    multi = 1
    value = long(0)
    for b in bits:
        value += b * multi
        multi *= 2
    return value


def bytes2dec(bytes, sz=8):
    return bin2dec(bytes2bin(bytes, sz))


##
# Convert a decimal value to an array of bits (MSB first), optionally
# padding the overall size to p bits.
def dec2bin(n, p=0):
    assert(n >= 0)
    retVal = []

    while n > 0:
       retVal.append(n & 1)
       n >>= 1

    if p > 0:
        retVal.extend([0] * (p - len(retVal)))
    retVal.reverse()
    return retVal


def dec2bytes(n, p=0):
    return bin2bytes(dec2bin(n, p))


##
# Convert a list of bits (MSB first) to a synch safe list of bits
# (section 6.2 of the ID3 2.4 spec.
def bin2synchsafe(x):
    n = bin2dec(x)
    if len(x) > 32 or n > 268435456:   # 2^28
        raise ValueError("Invalid value: %s" % str(x))
    elif len(x) < 8:
        return x

    bites = ""
    bites += chr((n >> 21) & 0x7f)
    bites += chr((n >> 14) & 0x7f)
    bites += chr((n >>  7) & 0x7f)
    bites += chr((n >>  0) & 0x7f)
    bits = bytes2bin(bites)
    assert(len(bits) == 32)

    return bits

def bytes2str(bites):
    s = bytes("")
    for b in bites:
        s += ("\\x%02x" % ord(b))
    return s


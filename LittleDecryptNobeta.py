#!/usr/bin/env python3

import argparse
import base64
import io
import sys
try:
	import Crypto.Cipher.AES as AES
except ImportError:
	print("cannot find library Crypto; try install with 'pip install "
		"pycryptodome '", file=sys.stderr)
	sys.exit(1)


def get_args():
	ap = argparse.ArgumentParser(description="""
Decrypt GameSave[0-3].dat and System.dat for viewing and editing or encrypt in
reverse. GameSave[0-3].dat store data in the corresponding game save slots;
System.dat stores global data (e.g. appearance) and achievement data (including
some gameplay stats). This script is independent to the web-based version, nor
vice-versa.""")
	ap.add_argument("input", type=str, nargs="?", default="-",
		help="input file [stdin]")
	ap.add_argument("--output", "-o", type=str, default="-",
		metavar="file",
		help="output file [stdout]")
	ap.add_argument("--encrypt", "-e", action="store_true",
		help="run encryption rather than decryption")
	# ap.add_argument("--neat-json", action="store_true",
	# help="output JSON in a easy-to-read format (only works in decryption "
	# "mode)")

	# parse args
	args = ap.parse_args()
	if args.input == "-":
		args.input = sys.stdin.buffer
	if args.output == "-":
		args.output = sys.stdout.buffer

	return args


class AesJsonIO(object):
	def __init__(self, key: bytes, iv: bytes, *ka, **kw):
		super().__init__(*ka, **kw)
		self.key = key
		self.iv = iv
		return

	@staticmethod
	def get_fp(f, *ka, factory=open, **kw) -> io.IOBase:
		if isinstance(f, io.IOBase):
			ret = f
		elif isinstance(f, str):
			ret = factory(f, *ka, **kw)
		else:
			raise TypeError("first argument of get_fp() must be io.IOBase or "
				"str, got '%s'" % type(f).__name__)
		return ret

	def run(self, ifile, ofile, *, encrypt=False) -> None:
		if encrypt:
			self.encrypt(ifile, ofile)
		else:
			self.decrypt(ifile, ofile)
		return

	def decrypt(self, ifile, ofile) -> None:
		with self.get_fp(ifile, "rb") as fp:
			enc_bytes = fp.read()
		cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
		dec_bytes = self.unpadding(cipher.decrypt(enc_bytes))
		with self.get_fp(ofile, "wb") as fp:
			fp.write(dec_bytes)
		return

	def encrypt(self, ifile, ofile) -> None:
		with self.get_fp(ifile, "rb") as fp:
			dec_bytes = fp.read()
		cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
		enc_bytes = cipher.encrypt(self.padding(dec_bytes))
		with self.get_fp(ofile, "wb") as fp:
			fp.write(enc_bytes)
		return

	@staticmethod
	def padding(b: bytes) -> bytes:
		# AES block size should be 16 in this case
		pad_len = AES.block_size - (len(b) % AES.block_size)
		pad_char = chr(pad_len).encode("ascii")
		return b + (pad_char * pad_len)

	@staticmethod
	def unpadding(b: bytes) -> bytes:
		pad_len = b[-1]  # should be an int
		return b[:-pad_len]


def main():
	args = get_args()
	o = AesJsonIO(
		key=base64.decodebytes(b"vckiTpRHOzjVf+5/+d9EIw=="),
		iv=base64.decodebytes(b"zXKcTMyXoZAtt4f0XXsQ2Q=="),
	)
	o.run(args.input, args.output, encrypt=args.encrypt)
	return


if __name__ == "__main__":
	main()

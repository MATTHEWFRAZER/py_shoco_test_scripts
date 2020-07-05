import ctypes

from shoco.compressor import Compressor
from shoco.decompressor import Decompressor
from shoco.model_trainer import train

with open("metamorphasis.txt", "rb") as f:
    data = f.read()

pack_count = 3

model_trainer_result = train([x.strip() for x in data.splitlines()], False)
compression_successor_table = model_trainer_result.compression_successor_table
decompression_successor_table = model_trainer_result.decompression_successor_table
packs = model_trainer_result.packs
min_char = model_trainer_result.min_char

compressor = Compressor(compression_successor_table, packs)
decompressor = Decompressor(decompression_successor_table, packs, min_char)

original_string = "bug insect jj"
original_length = len(original_string)
original = (ctypes.c_uint8 * original_length)()
for i, x in enumerate(original_string):
    original[i] = ord(x)

out = (ctypes.c_uint8 * original_length)()
len_of_newly_compressed = compressor.compress(original, original_length, out, original_length)

print(original_length, len_of_newly_compressed)
for i in range(original_length):
    print("ord", out[i])

print("HI")
out2 = (ctypes.c_uint8 * original_length)()

decompressor.decompress(out, len_of_newly_compressed, out2, original_length)

for i in range(original_length):
    print(chr(out2[i]))
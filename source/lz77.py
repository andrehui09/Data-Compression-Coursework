import os, sys, time, math
from bitarray import bitarray

def compress(file, windowSize):
    startTime = time.time()
    window = ""
    triples = []
    x=0
    
    bArray = bitarray()
    with open("input/" + file, "rb") as f:
        bArray.fromfile(f)
    bStr = bArray.to01()
    bOutput = ""
    
    if windowSize == 0:
        windowSize == len(bStr)
    
    dBits = math.ceil(len(bin(int(windowSize))[2:])/8)
    bOutput = ("0000000" + bin(dBits)[2:])[-8:]

    while (len(bStr) != 0):
        prefix = bStr[0]
        l = 1
        exist = window.find(prefix)
        while exist >= 0 and l < len(bStr) and l < 255:
            prefix += bStr[l]
            exist = window.find(prefix)
            l += 1
        
        if len(prefix) > 1:
            d = len(window) - window.find(prefix[:-1])
            l = len(prefix) - 1
            c = prefix[-1]
        else:
            d = 0
            l = 0
            c = prefix

        triples.append((d,l,c))

        d = ((dBits*"00000000") + bin(d)[2:])[-(dBits*8):]
        l = ("0000000" + bin(l)[2:])[-8:]
        bOutput += d + l + c

        window += prefix
        window = window[-windowSize:]
        bStr = bStr[len(prefix):]

    while len(bOutput)%8 != 0:
        bOutput += "0"
    
    with open("compressed/" + file + ".enc", "wb") as f:
        bOut = bitarray(bOutput)
        bOut.tofile(f)
    endTime = time.time()
    return [endTime - startTime, len(bOutput), len(bArray), len(bArray)/len(bOutput), triples]

def decompress(file):
    startTime = time.time()

    bArray = bitarray()
    with open("compressed/" + file, "rb") as f:
        bArray.fromfile(f)
    bArray = bArray.to01()
    triples = []
    dBits = int(bArray[0:8], 2) * 8
    i = 8
    text = ""
    while i < len(bArray):
        if i + dBits + 8 < len(bArray):
            d = int(bArray[i:i + dBits], 2)
            l = int(bArray[i + dBits:i + dBits + 8], 2)
            c = bArray[i + dBits + 8]
            triples.append((d,l,c))
            if l != 0:
                if l - d == 0:
                    text += text[-d:]
                else:
                    text += text[-d:l-d]
            text += c
        i += dBits + 9

    with open("decompressed/" + file[0:-4], "wb") as f:
        bitarray(text).tofile(f)

    endTime = time.time()
    return [endTime - startTime, triples]

def main(argv):
    if len(argv) != 3:
        return "Usage: python {} InputFile.ext WindowSize(0 to decompress only)".format(argv[0])
    file = argv[1]
    if not os.path.exists("input/" + file) and not os.path.exists("compressed/" + file):
        return "Input file is not in the corresponding folder: " + file
    if os.path.isdir(file):
        return "Input file is a directory: " + file
    window = int(argv[2])

    if window != 0:
        c = compress(file, window)
        d = decompress(file + ".enc")
        output = "\n  Filename: " + file + "\n  Window Size: " + str(window) + "\n\n  Compression Time: " + str(c[0]) + "s\n  Decompression Time: " + str(d[0]) + "s\n  Total Time: " + str(c[0]+d[0]) + "s\n\n  Original File Size: " + str(c[2]) + "bits\n  Compressed File Size: " + str(c[1]) + "bits\n  Compression Ratio: " + str(c[3]) + "bits\n\n  Please find the compressed file in the compressed folder, and the decompressed file in the decompressed folder."
    else:
        d = decompress(file)
        output = "\n  Filename: " + file + "\n  Window Size: " + str(window) + "\n\n  Decompression Time: " + str(d[0]) + "s\n\n  Please find the decompressed file in the decompressed folder."
    return output

if __name__ == "__main__":
    out = main(sys.argv)
    if out is not None:
        sys.exit(out)
    
    

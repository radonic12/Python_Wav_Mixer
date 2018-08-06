import wave
import array

def Audiomix():
    w1 = wave.open("path/to/audiofile1.wav")
    w2 = wave.open("path/to/audiofile2.wav")

    #get samples formatted as a string.
    samples1 = w1.readframes(w1.getnframes())
    samples2 = w2.readframes(w2.getnframes())


    #takes every 2 bytes and groups them together as 1 sample. ("123456" -> ["12", "34", "56"])
    samples1 = [samples1[i:i+2] for i in range(0, len(samples1), 2)]
    samples2 = [samples2[i:i+2] for i in range(0, len(samples2), 2)]

    #convert samples from strings to ints
    def bin_to_int(bin):
        as_int = 0
        for char in bin[::-1]: #iterate over each char in reverse (because little-endian)
            #get the integer value of char and assign to the lowest byte of as_int, shifting the rest up
            as_int <<= 8
            as_int += char
        return as_int

    samples1 = [bin_to_int(s) for s in samples1] #['\x04\x08'] -> [0x0804]
    samples2 = [bin_to_int(s) for s in samples2]

    #average the samples:
    samples_avg = [(s1+s2) for (s1, s2) in zip(samples1, samples2)]

    samples_array = array.array('i');
    samples_array.fromlist(samples_avg);
    
    wave_out = wave.open ("out.wav", "wb");
    wave_out.setnchannels(1)
    wave_out.setsampwidth(2)
    wave_out.setframerate(w1.getframerate()*4)
    wave_out.writeframes(samples_array)

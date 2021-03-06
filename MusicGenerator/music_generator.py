import math
import wave
import random
from array import array

import sys

CHORDS = {
    "Dm7": [38, 50, 53, 57, 60],
    "G7": [31, 50, 53, 55, 59],
    "Cmaj7": [36, 48, 52, 55, 59],
    "C6": [36, 48, 52, 57, 64],
    "C6th": [64, 60, 57, 55, 52, 48],
    "E13th": [64, 61, 59, 56, 54, 50, 44, 40],
    "A6th": [64, 61, 57, 54, 52, 49, 45, 42],
    "GDobro": [64, 59, 55, 50, 47, 43],
    "DMajor": [66, 62, 57, 54, 50, 38],
    "C#Minor": [64, 61, 56, 52, 50, 47]
}

# CHORDS = {
#     "Dm7": [38, 50, 53, 57, 60],
#     "G7": [31, 50, 53, 55, 59],
#     "Cmaj7": [36, 48, 52, 55, 59],
#     "C6": [36, 48, 52, 57, 64]
# }

# CHORDS = {
#     "C6th": [64, 60, 57, 55, 52, 48],
#     "E13th": [64, 61, 59, 56, 54, 50, 44, 40],
#     "A6th": [64, 61, 57, 54, 52, 49, 45, 42],
#     "GDobro": [64, 59, 55, 50, 47, 43],
#     "DMajor": [66, 62, 57, 54, 50, 38],
#     "C#Minor": [64, 61, 56, 52, 50, 47]
# }

# CHORDS = {
#     "major": [0, 4, 7, 12],
#     "minor": [0, 3, 7, 12],
#     "major7": [0, 4, 7, 11],
#     "minor7": [0, 3, 7, 10],
#     "minor75": [0, 3, 6, 10],
#     "dim": [0, 3, 6, 9],
#     "dom7": [0, 4, 7, 10],
#     "major9": [0, 4, 7, 11, 14],
#     "minor9": [0, 3, 7, 10, 14]
# }


# Jazzy
TYPE = 0


# Rock

class Scale(object):
    def __init__(self, note, length):
        self.note = note
        self.length = length

        self.released = False
        self.t = 0

        self.oscillator = oscillator(self.note)
        self.adsr = ADSREnvelope(0.1, 1.0, 0.7, 3.0)

    def __iter__(self):
        return self

    def next(self):
        if self.t >= self.length:
            self.released = True
            self.adsr.trigger_release()
        self.t += 1

        sample = next(self.adsr) * next(self.oscillator)
        #print(sample)
        return sample


class ADSREnvelope(object):
    """
    ADSR envelope generator class
    """

    RATIO = 1.0 - 1.0 / math.e

    def __init__(self, attack, decay, sustain, release):
        self.attacking = True
        self.released = False
        self.level = 0.0

        compute_coefficient = lambda time: 1.0 - math.exp(-1.0 / (time * 44100.0))
        # print(compute_coefficient)

        self.attack = compute_coefficient(attack)
        self.decay = compute_coefficient(decay)
        self.sustain = sustain
        self.release = compute_coefficient(release)

    def __iter__(self):
        return self

    def trigger_release(self):
        self.released = True

    def next(self):
        if self.released:
            self.level += self.release * (1.0 - (1.0 / self.RATIO) - self.level)
            if self.level < 0.0:
                # envelope finished
                raise StopIteration
        else:
            if self.attacking:
                self.level += self.attack * ((1.0 / self.RATIO) - self.level)
                if self.level > 1.0:
                    # attack phase finished
                    self.level = 1.0
                    self.attacking = False
            else:
                self.level += self.decay * (self.sustain - self.level)

        return self.level


def oscillator(pitch):
    """
    Generate a waveform at a given pitch
    """
    phi = 0.0
    frequency = (2.0 ** ((pitch - 69.0) / 12.0)) * 440.0
    delta = 2.0 * math.pi * frequency / 44100.0
    #print(delta)

    while True:
        yield math.sin(phi) + math.sin(2.0 * phi)
        phi += delta


def amplifier(gain, iterable):
    """
    Attenuate the input signal by a given gain factor
    """
    return (gain * sample for sample in iterable)


def chord_generator(iterable):
    """
    Converts chord symbols to a list of MIDI notes.
    """
    return (CHORDS[chord_symbol] for chord_symbol in iterable)


def comp_pattern_generator(pattern, iterable):
    """
    Return a chord pattern randomly from a request pattern type
    """
    randomValue = random.randint(0, 10)
    if pattern == 1:  # jazz
        return comp_pattern_generator_jazz(iterable)
    elif pattern == 0:  # happy
        if randomValue % 8 == 0:
            return comp_pattern_generator_happy0(iterable)
        elif randomValue % 7 == 0:
            return comp_pattern_generator_happy1(iterable)
        elif randomValue % 6 == 0:
            return comp_pattern_generator_happy2(iterable)
        elif randomValue % 5 == 0:
            return comp_pattern_generator_happy3(iterable)
        elif randomValue % 4 == 0:
            return comp_pattern_generator_happy4(iterable)
        elif randomValue % 3 == 0:
            return comp_pattern_generator_happy5(iterable)
        elif randomValue % 2 == 0:
            return comp_pattern_generator_happy6(iterable)
        elif randomValue % 1 == 0:
            return comp_pattern_generator_happy7(iterable)
        else:
            return comp_pattern_generator_happy0(iterable)
    elif pattern == 2:  # neutral
        if randomValue % 2 == 0:
            return comp_pattern_generator_neutral1(iterable)
        else:
            return comp_pattern_generator_neutral2(iterable)
    elif pattern == 3:  # emotional
        if randomValue % 4 == 0:
            return comp_pattern_generator_emotional1(iterable)
        elif randomValue % 3 == 0:
            return comp_pattern_generator_emotional2(iterable)
        elif randomValue % 2 == 0:
            return comp_pattern_generator_emotional3(iterable)
        elif randomValue % 1 == 0:
            return comp_pattern_generator_emotional4(iterable)
        else:
            return comp_pattern_generator_emotional1(iterable)
    elif pattern == 4:  # sad
        if randomValue % 2 == 0:
            return comp_pattern_generator_sad1(iterable)
        else:
            return comp_pattern_generator_sad2(iterable)
    elif pattern == 5:  # faces
        if randomValue % 7 == 0:
            return comp_pattern_generator_happy0(iterable)
        elif randomValue % 6 == 0:
            return comp_pattern_generator_happy1(iterable)
        elif randomValue % 5 == 0:
            return comp_pattern_generator_happy2(iterable)
        elif randomValue % 4 == 0:
            return comp_pattern_generator_happy3(iterable)
        elif randomValue % 3 == 0:
            return comp_pattern_generator_happy4(iterable)
        elif randomValue % 2 == 0:
            return comp_pattern_generator_happy5(iterable)
        elif randomValue % 1 == 0:
            return comp_pattern_generator_happy6(iterable)
        else:
            return comp_pattern_generator_neutral2(iterable)
    else:
        print("Unknown pattern")
        return comp_pattern_generator_jazz(iterable)


def comp_pattern_generator_jazz(iterable):
    """
    Converts a list of MIDI notes to (length, notes) tuples in a jazzy pattern.
    """
    for chord in iterable:
        yield (600, chord)
        yield (300, chord[0:1])
        yield (300, chord)
        yield (600, chord[0:1])
        yield (300, chord)
        yield (200, chord[0:1])


def comp_pattern_generator_happy0(iterable):
    """
    Converts a list of MIDI notes to (length, notes) tuples in a happy pattern.
    """
    for chord in iterable:
        yield (200, chord)
        yield (200, chord[0:1])
        yield (200, chord)
        yield (200, chord)
        yield (200, chord)
        yield (200, chord[0:1])


def comp_pattern_generator_happy1(iterable):
    """
    Converts a list of MIDI notes to (length, notes) tuples in a happy pattern.
    """
    for chord in iterable:
        yield (200, chord)
        yield (200, chord[0:1])
        yield (200, chord)
        yield (200, chord)
        yield (200, chord[0:2])
        yield (200, chord[0:1])


def comp_pattern_generator_happy2(iterable):
    """
    Converts a list of MIDI notes to (length, notes) tuples in a happy pattern.
    """
    for chord in iterable:
        yield (200, chord)
        yield (200, chord[0:1])
        yield (200, chord)
        yield (200, chord)
        yield (200, chord[0:3])
        yield (200, chord)


def comp_pattern_generator_happy3(iterable):
    """
    Converts a list of MIDI notes to (length, notes) tuples in a happy pattern.
    """
    for chord in iterable:
        yield (200, chord)
        yield (200, chord[0:1])
        yield (200, chord)
        yield (200, chord[0:2])
        yield (200, chord[0:3])
        yield (200, chord)


def comp_pattern_generator_happy4(iterable):
    """
    Converts a list of MIDI notes to (length, notes) tuples in a happy pattern.
    """
    for chord in iterable:
        yield (200, chord[0:2])
        yield (200, chord[0:1])
        yield (200, chord)
        yield (200, chord[0:2])
        yield (200, chord[0:3])
        yield (200, chord)


def comp_pattern_generator_happy5(iterable):
    """
    Converts a list of MIDI notes to (length, notes) tuples in a happy pattern.
    """
    for chord in iterable:
        yield (200, chord[0:2])
        yield (200, chord[0:1])
        yield (200, chord[0:3])
        yield (200, chord[0:2])
        yield (200, chord[0:3])
        yield (200, chord)


def comp_pattern_generator_happy6(iterable):
    """
    Converts a list of MIDI notes to (length, notes) tuples in a happy pattern.
    """
    for chord in iterable:
        yield (200, chord[0:2])
        yield (200, chord[0:1])
        yield (200, chord[0:3])
        yield (200, chord[0:2])
        yield (200, chord[0:3])
        yield (200, chord[0:2])


def comp_pattern_generator_happy7(iterable):
    """
    Converts a list of MIDI notes to (length, notes) tuples in a happy pattern.
    """
    for chord in iterable:
        yield (300, chord)
        yield (200, chord[2:3])
        yield (300, chord[0:2])
        yield (300, chord)
        yield (200, chord)
        yield (300, chord[2:3])


def comp_pattern_generator_emotional1(iterable):
    """
    Converts a list of MIDI notes to (length, notes) tuples in a emo pattern.
    """
    for chord in iterable:
        yield (400, chord[0:2])
        yield (400, chord[0:1])
        yield (400, chord[0:3])
        yield (400, chord[0:2])
        yield (400, chord[0:3])
        yield (400, chord[0:2])


def comp_pattern_generator_emotional2(iterable):
    """
    Converts a list of MIDI notes to (length, notes) tuples in a emo pattern.
    """
    for chord in iterable:
        yield (500, chord[0:2])
        yield (500, chord[0:1])
        yield (500, chord[0:3])
        yield (500, chord[0:2])
        yield (500, chord[0:3])
        yield (500, chord[0:2])


def comp_pattern_generator_emotional3(iterable):
    """
    Converts a list of MIDI notes to (length, notes) tuples in a emo pattern.
    """
    for chord in iterable:
        yield (500, chord[0:2])
        yield (200, chord[0:1])
        yield (500, chord[0:3])
        yield (200, chord[0:2])
        yield (500, chord[0:3])
        yield (200, chord[0:2])


def comp_pattern_generator_emotional4(iterable):
    """
    Converts a list of MIDI notes to (length, notes) tuples in a emo pattern.
    """
    for chord in iterable:
        yield (500, chord[1:2])
        yield (200, chord[0:1])
        yield (500, chord[2:3])
        yield (200, chord[1:2])
        yield (500, chord[2:3])
        yield (200, chord[1:2])


def comp_pattern_generator_neutral1(iterable):
    """
    Converts a list of MIDI notes to (length, notes) tuples in a neutral pattern.
    """
    for chord in iterable:
        yield (600, chord[2:3])
        yield (400, chord[1:2])
        yield (600, chord[0:1])
        yield (500, chord[3:4])
        yield (600, chord[2:3])
        yield (600, chord[3:4])


def comp_pattern_generator_neutral2(iterable):
    """
    Converts a list of MIDI notes to (length, notes) tuples in a neutral pattern.
    """
    for chord in iterable:
        yield (200, chord)
        yield (200, chord[0:5])
        yield (200, chord)
        yield (200, chord)
        yield (200, chord[0:5])
        yield (200, chord)


def comp_pattern_generator_sad1(iterable):
    """
    Converts a list of MIDI notes to (length, notes) tuples in a sad pattern.
    """
    for chord in iterable:
        yield (600, chord[0:1])
        yield (500, chord[2:3])
        yield (600, chord[0:1])
        yield (500, chord[3:4])
        yield (600, chord[0:1])
        yield (500, chord[3:4])


def comp_pattern_generator_sad2(iterable):
    """
    Converts a list of MIDI notes to (length, notes) tuples in a sad pattern.
    """
    for chord in iterable:
        yield (600, chord[1:3])
        yield (500, chord[1:2])
        yield (500, chord[1:2])
        yield (600, chord[2:4])
        yield (500, chord[2:3])
        yield (500, chord[2:4])


def scale_generator(iterable):
    """
    Converts a (length, notes) tuple into a (start time, list of scales) tuple
    """
    t = 0
    for length, pitches in iterable:
        scales = [Scale(pitch, length) for pitch in pitches]
        yield (t, scales)
        t += length


def scale_combiner(iterable):
    """
    Renders samples from scales and maintains a scale pool
    """
    t = 0.0
    stopping = False
    scale_pool = []
    scale_time, scale_list = next(iterable)

    while True:
        # add new scales to the pool
        while t >= scale_time:
            scale_pool.extend(scale_list)

            try:
                scale_time, scale_list = next(iterable)
            except StopIteration:
                scale_time = float("inf")
                stopping = True

        # pull samples from scales and mix them
        sample = 0.0
        pending_removal = []
        for scale in scale_pool:
            try:
                sample += next(scale)
            except StopIteration:
                # scale has stopped, remove it from the pool
                pending_removal.append(scale)

        # clean up pool
        for scale in pending_removal:
            scale_pool.remove(scale)

        # stop yielding if we're done
        if stopping and len(scale_pool) == 0:
            raise StopIteration

        yield sample
        t += 1000.0 / 44100.0


def conv_to_16bits(iterable):
    """
    Converts floating point audio signals to 16 bit integers
    """
    return (int(32767.0 * sample) for sample in iterable)


def generate(id, type=0, harmony=0, lenght=1):
    """
    Doing magic by transforming data into sounds
    """
    progression = []
    for i in range(0, lenght):
        chord = random.randint(0, len(CHORDS) - 1)
        progression.append(list(CHORDS.keys())[chord])

    #print(progression)
    #print(str(id))
    # create pipeline
    chords = chord_generator(progression)
    comp_pattern = comp_pattern_generator(type, chords)
    scales = scale_generator(comp_pattern)
    samples = scale_combiner(scales)
    attenuated_samples = amplifier(0.5, samples)
    output = conv_to_16bits(attenuated_samples)

    # prepare audio stream
    filename = "output-" + str(id) + ".wav"
    audiofile = wave.open(filename, "wb")
    audiofile.setnchannels(1)
    audiofile.setsampwidth(2)
    audiofile.setframerate(44100)

    # render samples
    output = list(output)
    audiofile.writeframes(array('h', output))
    audiofile.writeframes(array('h', output))
    audiofile.close()

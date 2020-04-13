#! /usr/bin/env python3

TEST_ONLY = False

import sys
from aubio import source, onset

# import os

#global onset_method, method_list

win_s = 512  # fft size
hop_s = win_s // 2  # hop size

filename = ""
kitname = ""

samplemode = 0
samplemode_name = 'CUT'
sourcemode = 0
sourcemode_name = 'NONE'
onset_method = 'hfc'
onset_division = 0
silence = -70.0
threshold = 0.3
sourceSlice = 'none'

sample_modes = {
    'CUT': 0,
    'ONCE': 1,
    'LOOP': 2,
    'STRETCH': 3
}



kit_head = [
    '<?xml version=\"1.0\" encoding=\"UTF-8\"?>',
    '<kit',
    '\tfirmwareVersion="3.0.4"',
    '\tearliestCompatibleFirmware="3.0.0"',
    '\tlpfMode="24dB"',
    '\tmodFXType="flanger"',
    '\tmodFXCurrentParam="feedback"',
    '\tcurrentFilterType="lpf">',
    '\t<delay',
    '\t\tpingPong="1"',
    '\t\tanalog="0"',
    '\t\tsyncLevel="7" />',
    '\t<compressor',
    '\t\tsyncLevel="6"',
    '\t\tattack="327244"',
    '\t\trelease="936" />',
    '\t<defaultParams',
    '\t\treverbAmount="0x80000000"',
    '\t\tvolume="0x3504F334"',
    '\t\tpan="0x00000000"',
    '\t\tsidechainCompressorShape="0xDC28F5B2"',
    '\t\tmodFXDepth="0x00000000"',
    '\t\tmodFXRate="0xE0000000"',
    '\t\tstutterRate="0x00000000"',
    '\t\tsampleRateReduction="0x80000000"',
    '\t\tbitCrush="0x80000000"',
    '\t\tmodFXOffset="0x00000000"',
    '\t\tmodFXFeedback="0x80000000">',
    '\t\t<delay',
    '\t\t\trate="0x00000000"',
    '\t\t\tfeedback="0x80000000" />',
    '\t\t<lpf',
    '\t\t\tfrequency="0x7FFFFFFF"',
    '\t\t\tresonance="0x80000000" />',
    '\t\t<hpf',
    '\t\t\tfrequency="0x80000000"',
    '\t\t\tresonance="0x80000000" />',
    '\t\t<equalizer',
    '\t\t\tbass="0x00000000"',
    '\t\t\ttreble="0x00000000"',
    '\t\t\tbassFrequency="0x00000000"',
    '\t\t\ttrebleFrequency="0x00000000" />',
    '\t</defaultParams>',
    '\t<soundSources>'
]

kit_tail = [

    '\t</soundSources>',
    '\t<selectedDrumIndex>0</selectedDrumIndex>',
    '</kit>'
]

sound_tail = [
    '\t\t\t<lfo1 type="triangle" syncLevel="0" />',
    '\t\t\t<lfo2 type="triangle" />',
    '\t\t\t<unison num="1" detune="8" />',
    '\t\t\t<compressor',
    '\t\t\t\tsyncLevel="6"',
    '\t\t\t\tattack="327244"',
    '\t\t\t\trelease="936" />',
    '\t\t\t<delay',
    '\t\t\t\tpingPong="1"',
    '\t\t\t\tanalog="0"',
    '\t\t\t\tsyncLevel="7" />',
    '\t\t\t<defaultParams',
    '\t\t\t\tarpeggiatorGate="0x00000000"',
    '\t\t\t\tportamento="0x80000000"',
    '\t\t\t\tcompressorShape="0xDC28F5B2"',
    '\t\t\t\toscAVolume="0x7FFFFFFF"',
    '\t\t\t\toscAPulseWidth="0x00000000"',
    '\t\t\t\toscBVolume="0x80000000"',
    '\t\t\t\toscBPulseWidth="0x00000000"',
    '\t\t\t\tnoiseVolume="0x80000000"',
    '\t\t\t\tvolume="0x4CCCCCA8"',
    '\t\t\t\tpan="0x00000000"',
    '\t\t\t\tlpfFrequency="0x7FFFFFFF"',
    '\t\t\t\tlpfResonance="0x80000000"',
    '\t\t\t\thpfFrequency="0x80000000"',
    '\t\t\t\thpfResonance="0x80000000"',
    '\t\t\t\tlfo1Rate="0x1999997E"',
    '\t\t\t\tlfo2Rate="0x00000000"',
    '\t\t\t\tmodulator1Amount="0x80000000"',
    '\t\t\t\tmodulator1Feedback="0x80000000"',
    '\t\t\t\tmodulator2Amount="0x80000000"',
    '\t\t\t\tmodulator2Feedback="0x80000000"',
    '\t\t\t\tcarrier1Feedback="0x80000000"',
    '\t\t\t\tcarrier2Feedback="0x80000000"',
    '\t\t\t\tmodFXRate="0x00000000"',
    '\t\t\t\tmodFXDepth="0x00000000"',
    '\t\t\t\tdelayRate="0x00000000"',
    '\t\t\t\tdelayFeedback="0x80000000"',
    '\t\t\t\treverbAmount="0x80000000"',
    '\t\t\t\tarpeggiatorRate="0x00000000"',
    '\t\t\t\tstutterRate="0x00000000"',
    '\t\t\t\tsampleRateReduction="0x80000000"',
    '\t\t\t\tbitCrush="0x80000000"',
    '\t\t\t\tmodFXOffset="0x00000000"',
    '\t\t\t\tmodFXFeedback="0x00000000">',
    '\t\t\t\t<envelope1',
    '\t\t\t\t\tattack="0x80000000"',
    '\t\t\t\t\tdecay="0xE6666654"',
    '\t\t\t\t\tsustain="0x7FFFFFD2"',
    '\t\t\t\t\trelease="0x80000000" />',
    '\t\t\t\t<envelope2',
    '\t\t\t\t\tattack="0xE6666654"',
    '\t\t\t\t\tdecay="0xE6666654"',
    '\t\t\t\t\tsustain="0xFFFFFFE9"',
    '\t\t\t\t\trelease="0xE6666654" />',
    '\t\t\t\t<patchCables>',
    '\t\t\t\t\t<patchCable',
    '\t\t\t\t\t\tsource="velocity"',
    '\t\t\t\t\t\tdestination="volume"',
    '\t\t\t\t\t\tamount="0x3FFFFFE8" />',
    '\t\t\t\t</patchCables>',
    '\t\t\t\t<equalizer',
    '\t\t\t\t\tbass="0x00000000"',
    '\t\t\t\t\ttreble="0x00000000"',
    '\t\t\t\t\tbassFrequency="0x00000000"',
    '\t\t\t\t\ttrebleFrequency="0x00000000" />',
    '\t\t\t</defaultParams>',
    '\t\t\t<arpeggiator',
    '\t\t\t\tmode="off"',
    '\t\t\t\tnumOctaves="2"',
    '\t\t\t\tsyncLevel="7" />',
    '\t\t\t<modKnobs>',
    '\t\t\t\t<modKnob controlsParam="pan" />',
    '\t\t\t\t<modKnob controlsParam="volumePostFX" />',
    '\t\t\t\t<modKnob controlsParam="lpfResonance" />',
    '\t\t\t\t<modKnob controlsParam="lpfFrequency" />',
    '\t\t\t\t<modKnob controlsParam="env1Release" />',
    '\t\t\t\t<modKnob controlsParam="env1Attack" />',
    '\t\t\t\t<modKnob controlsParam="delayFeedback" />',
    '\t\t\t\t<modKnob controlsParam="delayRate" />',
    '\t\t\t\t<modKnob controlsParam="reverbAmount" />',
    '\t\t\t\t<modKnob controlsParam="volumePostReverbSend" patchAmountFromSource="compressor" />',
    '\t\t\t\t<modKnob controlsParam="pitch" patchAmountFromSource="lfo1" />',
    '\t\t\t\t<modKnob controlsParam="lfo1Rate" />',
    '\t\t\t\t<modKnob controlsParam="pitch" />',
    '\t\t\t\t<modKnob controlsParam="stutterRate" />',
    '\t\t\t\t<modKnob controlsParam="bitcrushAmount" />',
    '\t\t\t\t<modKnob controlsParam="sampleRateReduction" />',
    '\t\t\t</modKnobs>',
    '\t\t</sound>'
]

method_list = ['default', 'energy', 'hfc', 'complex', 'phase', 'specdiff', 'kl', 'mkl', 'specflux', 'divide']

#
#Function: write individual sound (kit lane) to output file
#
def write_sound(s, e, m):
    output_file.write('\t\t<sound\n')
    output_file.write('\t\t\tname="SL' + str(slice) + '"\n')
    output_file.write('\t\t\tpolyphonic="audio"\n')
    output_file.write('\t\t\tvoicePriority="1"\n')
    output_file.write('\t\t\tmode="subtractive"\n')
    output_file.write('\t\t\tlpfMode="24dB"\n')
    output_file.write('\t\t\tmodFXType="none">\n')
    output_file.write('\t\t\t<osc1\n')
    output_file.write('\t\t\t\ttype="sample"\n')
    output_file.write('\t\t\t\tloopMode="' + str(m) + '"\n')
    output_file.write('\t\t\t\treversed="0"\n')
    output_file.write('\t\t\t\ttimeStretchEnable="0"\n')
    output_file.write('\t\t\t\ttimeStretchAmount="0"\n')
    output_file.write('\t\t\t\tfileName="' + filename[filename.find("SAMPLES"):] + '">\n')
    output_file.write('\t\t\t\t<zone\n')
    output_file.write('\t\t\t\t\tstartSamplePos="' + str(start) + '"\n')
    output_file.write('\t\t\t\t\tendSamplePos="' + str(end) + '" />\n')
    output_file.write("\t\t\t</osc1>\n")

    output_file.write('\t\t\t<osc2\n')
    output_file.write('\t\t\t\ttype="sample"\n')
    output_file.write('\t\t\t\tloopMode="0"\n')
    output_file.write('\t\t\t\treversed="0"\n')
    output_file.write('\t\t\t\ttimeStretchEnable="0"\n')
    output_file.write('\t\t\t\ttimeStretchAmount="0">\n')
    output_file.write("\t\t\t</osc2>\n")

    #
    #Output 'tail' of individual sound
    #
    for l in sound_tail:
        output_file.write(l)
        output_file.write("\n")


#
#   START
#

def main ():

    global onset_method, sourcemode_name, samplemode, samplemode_name, silence, threshold, onset_division
    global sourceSlice, output_file, start, end

    if len(sys.argv) < 2:
        print("\n")
        print("DELUGE SAMPLE 'SLICER' V0.30 by Neil Baldwin")
        print("--------------------------------------------")
        print("\n")
        print("PLEASE NOTE THIS ONLY WORKS WITH DELUGE OS V3.0 AND ABOVE!")
        print("\n")
        print("Usage: delslice.py [options] --input <input sample> --output <output kit>")
        print("\n")
        print("Run from root of your SD card!")
        print("You must specift paths relative to the root e.g. SAMPLES/LOOP/DRUM.WAV")
        print("\n")
        print("Please see README.TXT for full instructions.")
        print("\n")
        print("REQUIRED:")
        print("--input\t\tinput path/sample name")
        print("--output\toutput kit path/kit name")
        print("\n")
        print("OPTIONS FOR TRANSIENT DETECTION:")
        print("--method\ttransient scanning method - ENERGY, HFC (default)")
        print("\t\tCOMPLEX, PHASE, SPECDIFF, KL, MKL, SPECFLUX")
        print("--silence\tsilence level in DB (default -70.0)")
        print("\t\tSets silence level in dB under which there is no detections")
        print("\t\t-20.0 would eliminate most but the loudest signals, -90.0 would")
        print("\t\tdetect almost everything. Default -70.0")
        print("--threshold\tsensitivity for detection, typically 0.001 to 0.900")
        print("\t\tLower values imply more detection, higer values detect less. Default 0.3")
        print("\n")
        print("OPTIONAL NUMERICAL DIVISION:")
        print("--divide <n>\toverrides the transient detection, sets the split")
        print("\t\tpoints <n> equally through the sample instead")
        print("\n")
        print("OPTIONS FOR DELUGE OUTPUT")
        print("--sample\tdeluge sample type, CUT, ONCE, LOOP or STRETCH (default CUT)")
        print("\n")
        print("OPTIONS TO OUTPUT WHOLE SAMPLE AS EXTRA SLICE")
        print("--sourceSlice\teither 'first' or 'last'")
        print("--sourceMode\tCUT, ONCE, LOOP, STRETCH")
        print("\n")
        print("\n")

        sys.exit(1)

    #
    #Process command-line arguments
    #
    for arg in range(len(sys.argv)):
        if sys.argv[arg] == '--input':
            filename = sys.argv[arg + 1]

        if sys.argv[arg] == '--output':
            kitname = sys.argv[arg + 1]
        if sys.argv[arg] == '--sample':
            samplemode_name = str.upper(sys.argv[arg + 1])
            if samplemode_name in sample_modes:
                samplemode = sample_modes[samplemode_name]
            else:
                samplemode = 0
                samplemode_name = 'CUT'
        if sys.argv[arg] == '--method':
            onset_method = str.lower(sys.argv[arg + 1])

        if onset_method in method_list:
            onset_method = onset_method
        else:
            onset_method = 'hfc'

        if sys.argv[arg] == '--divide':
            onset_division = sys.argv[arg + 1]
        if sys.argv[arg] == '--silence':
            silence = sys.argv[arg + 1]
        if sys.argv[arg] == '--threshold':
            threshold = sys.argv[arg + 1]

        if sys.argv[arg] == '--sourceSlice':
            sourceSlice = str.lower(sys.argv[arg + 1])
            if sourceSlice != 'first':
                sourceSlice = 'last'
        if sys.argv[arg] == '--sourceMode':
            sourcemode_name = str.upper(sys.argv[arg + 1])
            if sourcemode_name in sample_modes:
                sourcemode = sample_modes[sourcemode_name]
            else:
                sourcemode = 0
                sourcemode_name = 'CUT'

    if sourcemode_name == 'NONE':
        sourcemode = samplemode
        sourcemode_name = samplemode_name

    if filename == "":
        print("No input file specified : use --input <sample path/name>")
    if kitname == "":
        print("No output file specified : use --output <kit path/name>")
    if (filename == "") or (kitname == ""):
        print("Error!")
        sys.exit(1)

    #Initialisation
    samplerate = 0
    s = source(filename, samplerate, hop_s)
    samplerate = s.samplerate

    #setup slice detection
    o = onset(onset_method, win_s, hop_s, samplerate)
    o.set_silence(float(silence))
    o.set_threshold(float(threshold))

    # list of onsets, in samples
    onsets = []

    if onset_division == 0:
        # total number of frames read
        total_frames = 0
        while True:
            samples, read = s()
            if o(samples):
                onsets.append(o.get_last())
            total_frames += read
            if read < hop_s: break
        onsets.append(total_frames)
    else:
        delta = s.duration / float(onset_division)
        read = 0
        while True:
            onsets.append(read)
            read = read + delta
            if read >= s.duration: break
        onsets.append(read)

    if TEST_ONLY:
        # print len(onsets)
        # for t in onsets:
        #	print t

        print(s.duration)

        sys.exit(1)

    if len(onsets) < 1:
        print("\nNo slices found with the setting you specified.\n")
        sys.exit(1)

    output_file = open(kitname, "w")
    for l in kit_head:
        output_file.write(l)
        output_file.write("\n")

    print("\n")

    if onset_division == 0:
        print("Method: " + str(onset_method))
        print("Threshold: " + str(o.get_threshold()))
        print("Silence: " + str(o.get_silence()))
    else:
        print("Method: Divide")

    print("Sample Type: " + samplemode_name)
    print("Source Slice Sample Type: " + sourcemode_name)
    print("\n")

    sourceStart = 0
    sourceEnd = s.duration
    print("Source Slice:", sourceSlice, sourceStart, sourceEnd)

    #
    # OUTPUT LOOP
    #
    sliceCount = 0
    if sourceSlice == 'first':
        start = sourceStart
        end = sourceEnd
        print("Slice {}:  {} - {}".format(sliceCount, start, end))
        write_sound(start, end, sourcemode)
        sliceCount += 1

    for slice in range(len(onsets) - 1):
        start = int(onsets[slice])
        end = int(onsets[slice + 1] - 1)
        print("Slice {}:  {} - {}".format(sliceCount, start, end))
        write_sound(start, end, samplemode)
        sliceCount += 1

    if sourceSlice == 'last':
        print("LAST SLICE!!!")
        start = sourceStart
        end = sourceEnd
        print("Slice {}:  {} - {}".format(sliceCount, start, end))
        write_sound(start, end, sourcemode)
        sliceCount += 1

    print("\nTotal slices written to '" + kitname + "' from sample '" + filename + "': " + str(sliceCount))
    print("\n")

    for l in kit_tail:
        output_file.write(l)
        output_file.write("\n")

    output_file.close()
    sys.exit()

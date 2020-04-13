========
delslice
========


.. image:: https://img.shields.io/pypi/v/delslice.svg
        :target: https://pypi.python.org/pypi/delslice

.. image:: https://img.shields.io/travis/neilbaldwin/delslice.svg
        :target: https://travis-ci.com/neilbaldwin/delslice

.. image:: https://readthedocs.org/projects/delslice/badge/?version=latest
        :target: https://delslice.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




Delslice


* Free software: MIT license
* Documentation: https://delslice.readthedocs.io.


DELSLICE.PY
===========

A Python script that scans single WAV sample and generate a single Deluge Kit automatically creating Start and End sample points for slices of the sample. Please note: when I refer to 'slicing a sample', no sample data is affected at all, the script only creates the Start and End points in the generated KIT file. All your samples will remain intact.

DISCLAIMER

THERE ARE PROBABLY BUGS! PLEASE BACK UP ANY IMPORTANT STUFF FROM YOUR DELUGE SD CARD BEFORE PLAYING WITH THIS. I'M BEING OVER DRAMATIC WITH THE CAPS BUT I TAKE NO RESPONSIBILITY IF THINGS GO WRONG. THANKS. BACK IT UP. GO ON.

Requirements:

I've tried as much as possible to make this work on both OSX (my own choice of OS) and Windows (tried running XP and Windows 10 in a virtual machine). 

CHANGE LOG:
-----------

V0.30 Refactored to take into account XML structure changes after OS V3.x. Also made some attempts at packaging the project as a Python package. See Installation instruction below.

V0.10 New feature. Option to add an extra slice containing the whole source sample to either be the first or last slice. Can also specify a separate Deluge sample mode for this extra slice.

V0.09 Minor changes to the path handling so that you no longer have to copy the script to your SD card. Unzip it into a folder on your computer and run it from there, specifying the drive/volume and full path for the sample input and kit output parameters.

	
INSTALLATION
-------------

pip3 install .



RUNNING THE SCRIPT
------------------

"python3 delslice"
	
The minimum you need to make the script work is this:

	delslice --input <sample filename> --output <output KIT name>
	
You'll need to specify the full path to your sample and output kit e.g. for OSX

	delslice --input /Volumes/DELUGE/SAMPLES/amen.wav --output /Volumes/DELUGE/KITS/KIT100.XML
	
or on Windows, for example (depending on what drive lettter is assigned to your SD card)


	delslice --input F:/SAMPLES/amen.wav --output F:/KITS/KIT100.XML

EXAMPLES
--------

	delslice --input F:/SAMPLES/LOOPS/DRUM01.WAV --method HFC --sample STRETCH -- output F:/KITS/KIT099.XML

will slice the DRUM01.WAV sample using the HFC (high frequency content) transient detection method and output the KIT099.XML file setting all the sample types to STRETCH

	delslice --input /Volumes/DELUGE/SAMPLES/LOOPS/DRUM01.WAV --divide 16 --sample ONCE --output /Volumes/DELUGE/KITS/KIT099.XML

will slice the DRUM01.WAV sample into 16 equal parts and output KIT099.XML setting the sample types to ONCE


OPTIONS
-------

REQUIRED PARAMETERS

--input	input path/sample name
--output	output kit path/kit name

OPTIONAL PARAMETERS

--sample	deluge sample output type
--method	transient scanning method
--silence	silence level in DB (default -70.0). See below.
--threshold	threshold level for detection (default 0.3). See below.
--divide 	divide sample equally

OPTIONAL OUTPUT OF SLICE CONTAINING WHOLE SAMPLE

--sourceSlice	either 'first' or 'last', defaults to none (no extra slice)
--sourceMode	Deluge sample mode for extra slice, can be set separately from other slices, defaults to same as others

SAMPLE -  sets the output Deluge sample type, CUT, ONCE, LOOP or STRETCH (default = CUT)

METHOD -  ENERGY, HFC, COMPLEX, PHASE, SPECDIFF, KL, MKL, SPECFLUX (default = HFC) see end of document for detail

DIVIDE - instead of using the various transient detection methods, DIVIDE will divide the sample equally into the number of slices specified.

THRESHOLD - Set the threshold value for the onset peak picking. Values are typically in the range [0.001, 0.900]. Lower threshold values imply more onsets detected. Increasing this threshold should reduce the number of incorrect detections. Defaults to 0.3.

SILENCE - Set the silence threshold, in dB, under which the onset will not be detected. A value of -20.0 would eliminate most onsets but the loudest ones. A value of -90.0 would select all onsets. Defaults to -90.0.


DETECTION METHODS	
-----------------

ENERGY
Energy based distance
This function calculates the local energy of the input spectral frame.

HFC (default)
High-Frequency content
This method computes the High Frequency Content (HFC) of the input spectral frame. The resulting function is efficient at detecting percussive onsets.

COMPLEX
Complex domain onset detection function
This function uses information both in frequency and in phase to determine changes in the spectral content that might correspond to musical onsets. It is best suited for complex signals such as polyphonic recordings.

PHASE
Phase based onset detection function
This function uses information both in frequency and in phase to determine changes in the spectral content that might correspond to musical onsets. It is best suited for complex signals such as polyphonic recordings.

SPECDIFF
Spectral difference onset detection function
Jonhatan Foote and Shingo Uchihashi. The beat spectrum: a new approach to rhythm analysis. In IEEE International Conference on Multimedia and Expo (ICME 2001), pages 881­884, Tokyo, Japan, August 2001.

KL
Kulback-Liebler onset detection function
Stephen Hainsworth and Malcom Macleod. Onset detection in music audio signals. In Proceedings of the International Computer Music Conference (ICMC), Singapore, 2003.

MKL
Modified Kulback-Liebler onset detection function
Paul Brossier, ``Automatic annotation of musical audio for interactive systems'', Chapter 2, Temporal segmentation, PhD thesis, Centre for Digital music, Queen Mary University of London, London, UK, 2006.

SPECFLUX
Spectral flux
Simon Dixon, Onset Detection Revisited, in ``Proceedings of the 9th International Conference on Digital Audio Effects'' (DAFx-06), Montreal, Canada, 2006.  


For more information on the --method parameter, see the Aubio page here:

https://aubio.org/manpages/latest/aubioonset.1.html



Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

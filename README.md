nprods/K11Consult
=================

IMPORTANT: Right at the moment, the project is in an "even-earlier-than-pre-alpha" state. It's published in Github just to make it easier to move the code between my devices. I also have very little experience with Python, so it's more a learning playground than any other thing.

nprods/K11Consult is a python project that uses pyserial to interact with the ECU of Nissan vehicles that utilise the Nissan Consult protocol.

It's a fork of the original project, but modded to run in a headless Raspberry Pi with a USB data reader cable.

The protocol reads and writes hex via a serial connection, reading in realtime the resultant data stream from the ECU. 

The script will be essentially in three parts; a thread that interacts with the ECU and make data conversion, a second thread logging data to a sqlite database and a third one sending the read data to a LCD display.

If you are interested in the project, please, contact me :)

#!/usr/bin/python3
import os
import socket
import threading
import pyaudio
import keyboard


class Client:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.name = input('Enter your nickname --> ')

        while 1:
            try:
                self.target_ip = input('Enter IP address of server --> ')
                self.target_port = 8080

                self.s.connect((self.target_ip, self.target_port))

                break
            except:
                print("Couldn't connect to server")

        chunk_size = 1024
        audio_format = pyaudio.paInt16
        channels = 1
        rate = 20000

        self.p = pyaudio.PyAudio()
        self.playing_stream = self.p.open(format=audio_format, channels=channels, rate=rate, output=True,
                                          frames_per_buffer=chunk_size)
        self.recording_stream = self.p.open(format=audio_format, channels=channels, rate=rate, input=True,
                                            frames_per_buffer=chunk_size)

        print("Connected to Server")

        # start threads
        receive_thread = threading.Thread(target=self.receive_server_data).start()
        self.send_data_to_server()

    def receive_server_data(self):
        while True:
            try:
                data = self.s.recv(1024)
                self.playing_stream.write(data)
            except:
                pass

    def send_data_to_server(self):
        try:
            self.s.sendall(self.name.encode())
        except:
            print("error occured")
            exit(1)
        while True:
                if keyboard.is_pressed('z'):
                    try:
                        data = self.recording_stream.read(1024)
                        self.s.sendall(data)
                    except:
                        continue
                if keyboard.is_pressed('x'):
                    print("Dropping connection")
                    self.s.close()
                    return


client = Client()

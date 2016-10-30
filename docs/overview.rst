
Sockets/Messenger
*****************

Sockets has evolved into a simple messaging program. One or more clients can
connect to a server and send messages to each other. All messages are plain
text, not encrypted, and therefore not suitable for serious use. Encryption may
come in the future.

Split into client and server, communicates using simple messages.
Not much else to say yet.

We are working on a graphical interface using Kivy. The program has an
interactive terminal interface right now, and works well, but we have run into
some limitations of terminal programs and have decided to switch.

Example Output
==============
Server::

    Starting server on port 50000...
    Received connection from client at 127.0.0.1:50000.
    [LOG] Renaming 127.0.0.1:50000 to Alice.
    Received connection from client at 127.0.0.1:50000.
    [LOG] Renaming 127.0.0.1:50000 to Bob.
    [LOG] Bob: 'hello'.
    [LOG] Sending messages to Alice.
    [LOG] Alice: 'hi there'.
    [LOG] Sending messages to Bob.
    [LOG] Bob: 'this is nice'.
    [LOG] Sending messages to Alice.

Client A::

    Starting client session targeting address localhost on port 50000...
    Bob: hello
    hi there
    Bob: this is nice

Client B::

    Starting client session targeting address localhost on port 50000...
    hello
    Alice: hi there
    this is nice

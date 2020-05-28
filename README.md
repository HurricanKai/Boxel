From the Original!

Boxel
======
Boxel is a near real-time pixelator and Minecraft codec.

Usage
======
Boxel pixelates and reduces the color pallete of images, websites and video at up to 24fps.

You can use it to make funky pixelated artwork from existing assets to display wherever you like.
By default, Boxel creates a stream of PNG images along with JSON messages that describe the image.

Boxel was built to act as a codec for Minecraft. You can use the data it creates to build boxelized images,
websites and video from blocks on a Minecraft server.

We've created a client library that makes it easy to connect Bukkit compatible Minecraft plugins to a Boxel server.
Check it out [here](https://github.com/HurricanKai/Boxel-Client)

Getting Started
================
Dependencies
-------------
Boxel depends on PhantomJS for rendering websites.
Installing on OSX with Homebrew is simple:
```bash
brew install phantomjs
```

Boxel expects to connect to Phantom remotely, so you should start it as below:
```bash
/usr/local/bin/phantomjs --webdriver=8910
```

We recommend using this Docker image to install and run your Phantom instance: [wernight/phantomjs](https://hub.docker.com/r/wernight/phantomjs/)

Boxel requires [Redis](http://redis.io) to send video data over PUB/SUB channels.
Redis can be installed via your package manager of choice:

```bash
# homebrew again
brew install redis

# or apt-get
sudo apt-get install redis-server
```

Finally, Boxel requires a WAMP router for service discovery. We use [crossbar](http://crossbar.io).
Crossbar can be installed via pip:

```bash
pip install crossbar
```

Installation
------------
After you've installed these dependencies, install boxel like any other Python package:
```bash
# using pip
pip install -e git+https://github.com/HurricanKai/Boxel.git#egg=boxel
```

Run it!
-------
Assuming you've got Redis, Phantom and a Crossbar router running you should be able to start the Boxel service like so:
```bash
# substitute the correct host/port for your redis server and crossbar router
boxel -W 50 -C palettes/5bit.yml video -R redis://localhost:6379/0 -U ws://localhost:8080/ws
```

Demo app
--------
The best place to start with Boxel is probably the demo app. This hasnt been found yet. Ill do one myself.

It provides docker containers for PhantomJS, Crossbar, Boxel, Redis, and an example web front-end that will get you a
Boxel service with just a few commands.

See [Boxel-client](https://github.com/HurricanKai/Boxel-Client) for examples of video and website rendering in Minecraft.

Contribute
===========
If you'd like to contribute, check out the [contributing guidelines](https://github.com/HurricanKai/Boxel/blob/master/CONTRIBUTING.md)

License
===========
This repository and its code are made available under a BSD 3-Clause license, which can be found [here](https://github.com/HurricanKai/Boxel/blob/master/LICENSE).


redis-rootkit
=============

The Redis security model is: “it’s totally insecure to let untrusted clients access the system, please protect it from the outside world yourself”. The reason is that.

Quickstart
----------
redis-rootkit require `redis-py <https://github.com/andymccurdy/redis-py>` to execute remote commands.

.. code-block:: bash
	
	$sudo pip install redis

.. code-block:: bash
	
	git clone https://github.com/gushitong/redis-rootkit

.. code-block:: bash
	
	cd redis-rootkit

.. code-block:: bash
	
	python redis-rootkit.py -r ~/.ssh/id_rsa.pub 127.0.0.1 


API Reference
-------------
* Usage: python redis-rootkit.py [OPTIONS] [TARGETS]
* -h --help: show redis-rootkit options.
* -p --port: target host port.
* -r --rsa-pub: rsa public key.


LICENSE
-------
MIT LICENSE



YoloLists
=========

KISS interface for Mailman2

Rant
----

In 2017, there is still no simple lightweight, free/open-source software to host mailing-lists. Solutions like Sympa and Mailman3 are designed for industrial scale use cases, and are too resource-hungry and/or too complex for the task they achieve. They are not suitable for self-hosting. A lot of small projects only need a handful of lists with a few hundreds of people max. They shouldn't have to install a software that permanently requires *several hundreds megabytes of RAM* - just to perform a task similar to what mail aliases do.

Meanwhile, Mailman2 remains kinda lightweight and simple (though could be improved..), but lacks a state-of-the-art, KISS web interface. 

YoloLists is a frustration-driven project that aims to propose such a web interface with Flask and Bootstrap.


Install / dev
-------------

Setup : 

```
git clone <thisrepo>
cd yololists
sudo apt-get install python-virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

Then launch the dev server :

```
./run_dev_server.sh
```



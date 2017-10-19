YoloLists
=========

KISS interface for Mailman2

Rant
----

In 2017, there is still no simple lightweight free/open-source software to host mailing-lists. Solutions like Sympa and Mailman3 are designed for industrial scale of mailing list hosting and are too resource-hungry and/or are too complex for the task they achieve. They are not suitable for self-hosting.

A lot of small projects only need a handful of lists with a few hundreds of people max. They shouldn't have to install a software that permanently requires several hundreds megabytes of RAM - just to perform a task similar to mail aliases do.

Meanwhile, Mailman2 remains kinda simple (though could be improved..), but lack of state-of-the-art web interface. YoloLists is a frustration-driven project that aims to propose such a web interface with Flask and Bootstrap.


Install / dev
-------------

Setup : 

```
git clone <thisrepo>
cd yololists
pip install --upgrade virtualenv
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
```

Then launch the dev server :

```
./run_dev_server.sh
```



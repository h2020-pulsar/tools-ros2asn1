ros2asn1
========
Provides a Python script and a module that checks the ROS types 
available in the system and generates a set of equivalent ASN.1 types.
Requires ROS to be installed.

License
-------
GPLv2

Installation
------------
From the build directory, run cmake .., then make install.

Run
----
First source your ROS environement and catkin workspace.
To convert messages and services from all packages to ASN1 :
```
ros2asn1_generate /path/to/output/directory
```
To convert messages and services from specific packages : 
```
ros2asn1_generate /path/to/output/directory package1 package2 ... packageN
```

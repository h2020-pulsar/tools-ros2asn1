# H2020 ESROCOS Project
# Company: GMV Aerospace & Defence S.A.U.
# Licence: GPLv2

"""This module provides functions to import ROS types to ESROCOS.

The ROS types are read from the local install and converted to 
equivalent ASN.1 data types for use in TASTE.

"""

from RosAsn1Generator import RosAsn1Generator
import rosmsg
import rospkg
import os
from mako.template import Template
import sys

def load_template(filename):
    '''
    Load a mako template, given its file name, from the templates directory.
    '''
    path = os.path.join(os.path.dirname(__file__), 'templates', filename)
    return Template(filename=path)
    

def process_all_messages(out_dir,packages_to_process=[]):
    '''Process all available ROS messages and generate ASN.1 types.
    For each package, one .asn file is created with one type per message.
    Additionally, if the message contains variable-sized elements, a
    userdefs-*.asn file is created with parametrized size defaults.
    '''
   
    rospack = rospkg.RosPack()

    asn_template = load_template('package.asn.mako')
    userdefs_template = load_template('userdefs.asn.mako')

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    # Find packages with messages and services
    existing_packages = [pkg for pkg, _ in rosmsg.iterate_packages(rospack, rosmsg.MODE_MSG)]
    for pkg, _ in rosmsg.iterate_packages(rospack, rosmsg.MODE_SRV):
        if pkg not in existing_packages:
            existing_packages.append(pkg)
    existing_packages = sorted(existing_packages)

    #check that packages given in input exists
    if packages_to_process:
        for pkg in packages_to_process:
            if pkg not in existing_packages:
                print("process_all_messages : input package {} does not exist".format(pkg))
                sys.exit(-1)
    #if no package specified, process all of them
    else:
        print("Processing all packages")
        packages_to_process = existing_packages

    for pkg in packages_to_process:
        try :  
            print('Creating ASN.1 types for {}'.format(pkg))
            
            pkg_obj = RosAsn1Generator(rospack, pkg)
            # ASN.1 types "pkg.asn"
            asn_txt = asn_template.render(pkg=pkg_obj)
        except:
            print("Error occured while processing {} package. Unabled to convert to ASN1".format(pkg))
            continue
        out_file1 = os.path.join(out_dir, pkg+'.asn')
        with open(out_file1, 'w') as fd:
            fd.write(asn_txt)

        # Size constants for variable-sized types "userdefs-pkg.asn"
        userdefs_txt = userdefs_template.render(pkg=pkg_obj)

        out_file2 = os.path.join(out_dir, 'userdefs-'+pkg+'.asn')
        with open(out_file2, 'w') as fd:
            fd.write(userdefs_txt)
        
    return

"""
This tests the basic properties
"""

import os
import pytest
import json
import argparse
import imp

from os import path
#import radical.utils.logger as rul
#from repex_utils.replica_cleanup import *
#from repex_utils.parser import parse_command_line

from pilot_kernels.pilot_kernel_pattern_s_multi_d_sc  import PilotKernelPatternSmultiDsc
from pilot_kernels.pilot_kernel_pattern_s_multi_d_scg import PilotKernelPatternSmultiDscg
from pilot_kernels.pilot_kernel_pattern_a_multi_d     import PilotKernelPatternAmultiD

from amber_kernel.kernel_pattern_s import KernelPatternS


@pytest.fixture(scope="class")
def repex_file_setup(fname):  
    from amber_kernel.kernel_pattern_s import KernelPatternS
    work_dir_local = (os.getcwd()+"/inputs")
    #print work_dir_local
    with open("inputs/%s"%fname) as data_file:
        inp_file = json.load(data_file)

    with open("inputs/stampede.json") as config_file:
        rconfig = json.load(config_file)

    
    return inp_file, rconfig, work_dir_local

@pytest.fixture(scope="class")
def repex_initialize(fname):
    from amber_kernel.kernel_pattern_s import KernelPatternS
    inp_file, rconfig, work_dir_local = repex_file_setup(fname)
    n = inp_file["dim.input"]["d1"]["number_of_replicas"]
    md_kernel    = KernelPatternS( inp_file, rconfig, work_dir_local )
    print md_kernel.work_dir_local
    print md_kernel.input_folder
    print md_kernel.amber_coordinates_path
    a = md_kernel.initialize_replicas()
    return md_kernel, a    


class Testbasic(object):
	#def test_import(self):
	#	from amber_kernel.kernel_pattern_s import KernelPatternS

    def test_try(self,cmdopt):
        fname = cmdopt
        #from amber_kernel.kernel_pattern_s import KernelPatternS
        inp_file, rconfig, work_dir_local = repex_file_setup(fname)
        #print cmdopt

        #if args.group_exe == "False""
        assert inp_file['remd.input'].get('group_exec') == 'False'
        #else:
            #assert inp_file['remd.input'].get('group_exec') == 'True'
            
    def test_name(self,cmdopt):
        fname = cmdopt
    	from amber_kernel.kernel_pattern_s import KernelPatternS
        md_kernel, a = repex_initialize(fname)
        print md_kernel.name
        assert md_kernel.name == 'amber-pattern-s-3d'

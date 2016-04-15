"""
This tests the basic properties
"""

import os
import pytest
import json

from os import path
import pilot_kernels


@pytest.fixture(scope="class")
def repex_file_setup():  
    from amber_kernel.kernel_pattern_s import KernelPatternS
    work_dir_local = (os.getcwd()+"/inputs")
    #print work_dir_local
    with open("inputs/tuu_remd_ace_ala_nme.json") as data_file:
        inp_file = json.load(data_file)

    with open("inputs/stampede.json") as config_file:
        rconfig = json.load(config_file)

    
    return inp_file, rconfig, work_dir_local

@pytest.fixture(scope="class")
def repex_initialize():
    from amber_kernel.kernel_pattern_s import KernelPatternS
    inp_file, rconfig, work_dir_local = repex_file_setup()
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

    def test_try(self):
        #from amber_kernel.kernel_pattern_s import KernelPatternS
        inp_file, rconfig, work_dir_local = repex_file_setup()
        assert inp_file['remd.input'].get('group_exec') == 'False'


    def test_name(self):
    	from amber_kernel.kernel_pattern_s import KernelPatternS
        md_kernel, a = repex_initialize()
        assert md_kernel.name == 'amber-pattern-s-3d'

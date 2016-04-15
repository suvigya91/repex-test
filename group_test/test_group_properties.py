import os
import pytest
import json
import radical.utils.logger as rul
from os import path

import radical.utils.logger as rul
import pilot_kernels
from pilot_kernels.pilot_kernel_pattern_s_multi_d_sc import PilotKernelPatternSmultiDsc
from pilot_kernels.pilot_kernel_pattern_s_multi_d_scg import PilotKernelPatternSmultiDscg

from amber_kernel.kernel_pattern_s import KernelPatternS

@pytest.fixture(scope="class")
def repex_file_setup():
    work_dir_local = (os.getcwd()+"/inputs")
    with open("inputs/tuu_remd_ace_ala_nme.json") as data_file:
        inp_file = json.load(data_file)

    with open("inputs/stampede.json") as config_file:
        rconfig = json.load(config_file)

    
    return inp_file, rconfig, work_dir_local

@pytest.fixture(scope="class")
def replica_num():
    with open("inputs/tuu_remd_ace_ala_nme.json") as data_file:
        inp_file = json.load(data_file)

    d1 = int(inp_file["dim.input"]["d1"]["number_of_replicas"])
    d2 = int(inp_file["dim.input"]["d2"]["number_of_replicas"])
    d3 = int(inp_file["dim.input"]["d3"]["number_of_replicas"])

    return d1,d2,d3

@pytest.fixture(scope="class")
def max_replica(d1,d2,d3):
    temp = []
    temp.append(d1)
    temp.append(d2)
    temp.append(d3)
    print temp
    temp = sorted(temp)
    print temp
    return temp[1],temp[2]
    
@pytest.fixture(scope="class")
def repex_initialize():
    inp_file, rconfig, work_dir_local = repex_file_setup()
    n = inp_file["dim.input"]["d1"]["number_of_replicas"]
    md_kernel    = KernelPatternS( inp_file, rconfig, work_dir_local )
    a = md_kernel.initialize_replicas()
    return md_kernel, a    

@pytest.fixture(scope="class")
def repex_initialize_shared_data():
    inp_file, rconfig, work_dir_local = repex_file_setup()
    n = inp_file["dim.input"]["d1"]["number_of_replicas"]
    md_kernel    = KernelPatternS( inp_file, rconfig, work_dir_local )
    a = md_kernel.initialize_replicas()
    md_kernel.prepare_shared_data(a)
    return md_kernel,a    


class Test_replica_tests(object):
    def test_initialize_replica_id(self):
        md_kernel, a = repex_initialize()
	d1,d2,d3 = replica_num()

	test_out = range(d1*d2*d3)
	replica_output = []
	for i in range(0,len(a)):
            replica_output.append(a[i].id)
	    #print a[i].group_idx

	print replica_output
	print test_out
	assert sorted(replica_output) == sorted(test_out)

    def test_total_group(self):
        md_kernel, a = repex_initialize()
        replica_output = []
        for i in range(0,len(a)):
            replica_output.append(a[i].group_idx)

        d1,d2,d3 = replica_num()
        max1,max2 = max_replica(d1,d2,d3)
        print max1*max2
        assert max(max(replica_output))+1 == (max1*max2)

class Test_groups(object):
    def test_group_d1(self):
        md_kernel, a = repex_initialize()
        d1,d2,d3 = replica_num()
        temp = [[] for x in xrange(d2*d3)]
        test_out = []
        #test_out = [2,2,2,2]
        for i in range(d2*d3):
            test_out.append(d1)
        print test_out
        i=0
        
        if i < d2*d3:
            for x in temp:
                for r in a:
                    if (r.group_idx[0]==i):
                        x.append(r)
                i = i+1
        
        num_out = []
        for x in temp:
            num_out.append(len(x))
        print num_out
        assert num_out == test_out


    def test_group_d2(self):
        md_kernel, a = repex_initialize()
        d1,d2,d3 = replica_num()
        temp = [[] for x in xrange(d1*d3)]
        test_out = []
        #test_out = [2,2,2,2]
        for i in range(d1*d3):
            test_out.append(d2)
        print test_out
        i=0
        
        if i < d1*d3:
            for x in temp:
                for r in a:
                    if (r.group_idx[1]==i):
                        x.append(r)
                i = i+1
        
        num_out = []
        for x in temp:
            num_out.append(len(x))
        print num_out
        assert num_out == test_out


    def test_group_d3(self):
        md_kernel, a = repex_initialize()
        d1,d2,d3 = replica_num()
        temp = [[] for x in xrange(d1*d2)]
        test_out = []
        #test_out = [2,2,2,2]
        for i in range(d1*d2):
            test_out.append(d3)
        print test_out
        i=0
        
        if i < d1*d2:
            for x in temp:
                for r in a:
                    if (r.group_idx[2]==i):
                        x.append(r)
                i = i+1
        
        num_out = []
        for x in temp:
            num_out.append(len(x))
        print num_out
        assert num_out == test_out



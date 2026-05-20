TESTID = "fig_slab"
import sys 
sys.path.append("..") 
from labcommon import *

test_name0 = "Ref"
exr_filename0 = "results/%s_%s.exr " % (TESTID, test_name0)
cmd = "..\\..\\mts1\\cbuild\\bin\\mitsuba.exe "
cmd += "slab_pcp.xml "
cmd += "-o %s " % exr_filename0
cmd += "-Dspp=16384 "
cmd += "-Dintegrator=sppm "

# t = my_run_cmd(TESTID, cmd, test_name0, instant=True)
# print(t)
# quit()

test_name0 = "UPSMCMC"
exr_filename0 = "results/%s_%s.exr " % (TESTID, test_name0)
cmd = "..\\..\\mts1\\cbuild\\bin\\mitsuba.exe "
cmd += "slab_pcp.xml "
cmd += "-o %s " % exr_filename0
cmd += "-Dspp=25 "
cmd += "-Dintegrator=upsmcmc "

# t = my_run_cmd(TESTID, cmd, test_name0, instant=True)
# print(t)

test_name0 = "SPPM"
exr_filename0 = "results/%s_%s.exr " % (TESTID, test_name0)
cmd = "..\\..\\mts1\\cbuild\\bin\\mitsuba.exe "
cmd += "slab_pcp.xml "
cmd += "-o %s " % exr_filename0
cmd += "-Dspp=130 "
cmd += "-Dintegrator=sppm "

# t = my_run_cmd(TESTID, cmd, test_name0, instant=True)
# print(t)
# quit()

test_name0 = "Bounded"
exr_filename0 = "results/%s_%s.exr " % (TESTID, test_name0)
cmd = "..\\..\\mts1\\cbuild\\bin\\mitsuba.exe "
cmd += "slab_pcp.xml "
cmd += "-DuseResultant=false -DmethodMask=0 -DdistrPath=../../results/sample_map.txt "
cmd += "-o %s " % exr_filename0
cmd += "-Dspp=2 -Dforce_gamma=70 "

t = my_run_cmd(TESTID, cmd, test_name0, instant=True)
print(t)
# quit()
test_name0 = "BoundedSMSU"
exr_filename0 = "results/%s_%s.exr " % (TESTID, test_name0)
cmd = "..\\..\\mts1\\cbuild\\bin\\mitsuba.exe "
cmd += "slab_pcp.xml "
cmd += "-DuseResultant=false -DmethodMask=9999 -DdistrPath=../../results/sample_map.txt "
cmd += "-o %s " % exr_filename0
cmd += "-Dspp=2 -Dforce_gamma=70 -p 32 "

# t = my_run_cmd(TESTID, cmd, test_name0, instant=True)
# print(t)
# quit()

test_name1 = "Enum"
exr_filename1 = "results/%s_%s.exr " % (TESTID, test_name1)
cmd = "..\\..\\mts1\\cbuild\\bin\\mitsuba.exe "
cmd += "slab_pcp.xml "
cmd += "-DuseResultant=false -DmethodMask=9999 "
cmd += "-o %s " % exr_filename1
cmd += "-Dspp=32 "
# t = my_run_cmd(TESTID, cmd, test_name1, instant=True)
# print(t)

test_name1 = "Uniform"
exr_filename1 = "results/%s_%s.exr " % (TESTID, test_name1)
cmd = "..\\..\\mts1\\cbuild\\bin\\mitsuba.exe "
cmd += "slab_pcp.xml "
cmd += "-DuseResultant=false -DmethodMask=-1 "
cmd += "-o %s " % exr_filename1
cmd += "-Dspp=26 -p 24 "

# t = my_run_cmd(TESTID, cmd, test_name1, instant=True)
# print(t)

test_name2 = "SMS"
mitsuba2_cmd = "..\\..\\mts\\build\\dist\\mitsuba.exe -m scalar_rgb "
exr_filename2 = "results/%s_%s.exr " % (TESTID, test_name2)
cmd = mitsuba2_cmd 
cmd += "slab_mpg.xml "
cmd += "-o %s " % exr_filename2
cmd += f"-Dtimeout=30 " 
cmd += f"-Dtrain_auto=false " 

# t = my_run_cmd(TESTID, cmd, test_name2, instant=False)
# print(t)

test_name2 = "MPG"
mitsuba2_cmd = "..\\..\\mts\\build\\dist\\mitsuba.exe -m scalar_rgb "
exr_filename2 = "results/%s_%s.exr " % (TESTID, test_name2)
cmd = mitsuba2_cmd 
cmd += "slab_mpg.xml "
cmd += "-o %s " % exr_filename2
cmd += f"-Dtimeout=30 " 
cmd += f"-Dtrain_auto=true " 

# t = my_run_cmd(TESTID, cmd, test_name2, instant=False)
# print(t)

test_name3 = "BDPT"
exr_filename3 = "results/%s_%s.exr " % (TESTID, test_name3)
cmd = "..\\..\\mts1\\cbuild\\bin\\mitsuba.exe "
cmd += "slab_pcp.xml "
cmd += "-o %s " % exr_filename3
cmd += "-Dintegrator=bdpt "
cmd += f"-Dspp={256} "
cmd += "-p 16 "
# t = my_run_cmd(TESTID, cmd, test_name3, instant=True)

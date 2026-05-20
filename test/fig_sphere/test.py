TESTID = "fig_sphere"
import sys

sys.path.append("..")
from labcommon import *

test_name0 = "Bounded"
exr_filename0 = "results/%s_%s.exr " % (TESTID, test_name0)
cmd = "..\\..\\mts1\\cbuild\\bin\\mitsuba.exe "
cmd += "sphere_pcp.xml "
cmd += "-DuseResultant=true -DmethodMask=0 "
# cmd += "-DdistrPath=../../results/sample_map.txt "
cmd += "-DdistrPath=../../data/s.obj "
cmd += "-o %s " % exr_filename0
cmd += "-Dspp=30 "
cmd += "-Dtimeout=0 "
# print(cmd)

t = my_run_cmd(TESTID, cmd, test_name0, instant=True)
print(t)
quit()

test_name1 = "Enum"
exr_filename1 = "results/%s_%s.exr " % (TESTID, test_name1)
cmd = "..\\..\\mts1\\cbuild\\bin\\mitsuba.exe "
cmd += "sphere_pcp.xml "
cmd += "-DuseResultant=true -DmethodMask=0 "
cmd += "-o %s " % exr_filename1
cmd += "-Dspp=1 "

# t = my_run_cmd(TESTID, cmd, test_name1, instant=True)
# print(t)
# quit()

test_name2 = "SMS"
mitsuba2_cmd = "..\\..\\mts\\build\\dist\\mitsuba.exe -m scalar_rgb "
exr_filename2 = "results/%s_%s.exr " % (TESTID, test_name2)
cmd = mitsuba2_cmd
cmd += "sphere_mpg.xml "
cmd += "-o %s " % exr_filename2
cmd += f"-Dtimeout=40 "
cmd += f"-Dtrain_auto=false "

t = my_run_cmd(TESTID, cmd, test_name2, instant=False)
print(t)

test_name2 = "MPG"
mitsuba2_cmd = "..\\..\\mts\\build\\dist\\mitsuba.exe -m scalar_rgb "
exr_filename2 = "results/%s_%s.exr " % (TESTID, test_name2)
cmd = mitsuba2_cmd
cmd += "sphere_mpg.xml "
cmd += "-o %s " % exr_filename2
cmd += f"-Dtimeout=40 -Dselective=true "
cmd += f"-Dtrain_auto=true "

t = my_run_cmd(TESTID, cmd, test_name2, instant=True)
print(t)

test_name0 = "UPSMCMC"
exr_filename0 = "results/%s_%s.exr " % (TESTID, test_name0)
cmd = "..\\..\\mts1\\cbuild\\bin\\mitsuba.exe "
cmd += "sphere_pcp.xml "
cmd += "-o %s " % exr_filename0
cmd += "-Dspp=99999 -Dtimeout=40 "
cmd += "-DinitialRadius=0.5 "
cmd += "-Dintegrator=upsmcmc "

# t = my_run_cmd(TESTID, cmd, test_name0, instant=False)
# print(t)

test_name0 = "SPPM"
exr_filename0 = "results/%s_%s.exr " % (TESTID, test_name0)
cmd = "..\\..\\mts1\\cbuild\\bin\\mitsuba.exe "
cmd += "sphere_pcp.xml "
cmd += "-o %s " % exr_filename0
cmd += "-Dspp=180 "
cmd += "-Dintegrator=sppm"

# t = my_run_cmd(TESTID, cmd, test_name0, instant=False)
# print(t)
# quit()

test_name1 = "Ref"
exr_filename1 = "results/%s_%s.exr " % (TESTID, test_name1)
cmd = "..\\..\\mts1\\cbuild\\bin\\mitsuba.exe "
cmd += "sphere_pcp.xml "
cmd += "-DuseResultant=true -DmethodMask=0 "
cmd += "-o %s " % exr_filename1
cmd += "-Dspp=24 -p 28 "
# t = my_run_cmd(TESTID, cmd, test_name1, instant=True)
# print(t)

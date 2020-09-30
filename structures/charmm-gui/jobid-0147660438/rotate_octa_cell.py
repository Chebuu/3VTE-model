#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
PANEL Nicolas, March 2015
BIOC, Ecole Polytechnique Palaiseau, FRANCE

This file: rotate_pdb.py

This scripts modifies NAMD xsc files to be constitent with the NAMD cell 
orientation convention (ie aligned with X-axis) and performs a rotation 
of the corresponding pdb/CHARMM crd

Command line:
rotate_pdb.py -x streamfile [-p pdbfile -c crdfile -o outputprefix]
"""

###############################################################################
# Libraries
##############################
from __future__ import print_function
import numpy as np
import re
import argparse
import copy


###############################################################################
# Classes
##############################

class Atom:
    """ Class describing atoms contained in a pdb file """
    def __init__(self,pdbline=None):
        self.type = ""   # Atom type : ATOM or HETATM
        self.num = 0     # Atom number
        self.atmn = ""   # Atom name
        self.alter = ""  # Alternative position
        self.resn = ""   # Residue name
        self.chain = ""  # chain id
        self.resnum = 0  # residue number
        self.insert = "" # code for insertion of residues
        self.x = 0.      # x coordinate
        self.y = 0.      # y coordinate
        self.z = 0.      # z coordinate
        self.occ = 0.    # occupancy
        self.temp = 0.   # temp factor
        self.segid = ""  # segment id
        self.resid = 0   # residue id
        self.elem = ""   # element symbol
        self.charge = "" # charge

        if pdbline:
            self.set(pdbline)

    def setpdb(self,line, pnum = 0):
        """ Sets atom from PDB line"""

        re_float = re.compile("^ *-?[0-9]+\.[0-9]+ *$")
        re_int = re.compile("^ *-?[0-9]+ *$")
        attr = ['type','num','atmn','alter','resn','chain','resnum','insert',\
        'x','y','z','occ','temp','segid','elem','charge']
        lim = [[0,6],[6,11],[12,16],[16,17],[17,20],[21,22],[22,26],[26,27],\
        [30,38],[38,46],[46,54],[54,60],[60,66],[72,76],[76,78],[78,80]]

        for i in range(len(attr)):
            try:
                field = line[lim[i][0]:lim[i][1]]
            except:
                pass
            if re_float.match(field):
                setattr(self,attr[i],float(field))
            elif re_int.match(field):
                setattr(self,attr[i],int(field))
            else:
                if i == 1:
                    field = pnum + 1
                    setattr(self,attr[i],int(field))
                else:
                    setattr(self,attr[i],field.rstrip())

        #Add chain if not in pdb;
        if self.segid == "":
            self.segid = "PRO"+self.chain



    def setcrd(self,line):
        """ Sets atom from CHARMM crd line"""

        re_float = re.compile("^ *-?[0-9]+\.[0-9]+ *$")
        re_int = re.compile("^ *-?[0-9]+ *$")
        attr = ['num','resnum','resn','atmn','x','y','z','segid','resid','temp']
        lim = [[0,10],[11,20],[22,31],[32,39],[40,60],[60,80],[80,100],[102,106],[112,120],[120,140]]

        for i in range(len(attr)):
            try:
                field = line[lim[i][0]:lim[i][1]]
            except:
                pass
            if re_float.match(field):
                setattr(self,attr[i],float(field))
            elif re_int.match(field):
                setattr(self,attr[i],int(field))
            else:
                setattr(self,attr[i],field.strip())

        #Add atom type for pdb output:
        self.type='ATOM'

    def pdb_format(self):
        """ Returns a CHARMM formated line"""

        if self.num >= 100000:
            return "%-6s%5s %-4s%1s%4s%1s%4d%1s   %8.3f%8.3f%8.3f%6.2f%6.2f      %-4s%2s%2s\n" \
                % (self.type, '*****', self.atmn, self.alter, self.resn, self.chain, self.resnum,\
                self.insert, self.x, self.y, self.z, self.occ, self.temp, self.segid ,self.elem, self.charge)
        else:
            return "%-6s%5d %-4s%1s%4s%1s%4d%1s   %8.3f%8.3f%8.3f%6.2f%6.2f      %-4s%2s%2s\n" \
                % (self.type, self.num, self.atmn, self.alter, self.resn, self.chain, self.resnum,\
                self.insert, self.x, self.y, self.z, self.occ, self.temp, self.segid ,self.elem, self.charge)

    def crd_format(self):
        """ Returns a CHARMM formated line"""

        return "%10d %9d  %-9s %-8s %19.10f %19.10f %19.10f  %-9s %-8d %19.10f\n"\
            % (self.num,self.resnum,self.resn,self.atmn,self.x,self.y,self.z,\
            self.segid,self.resid,self.temp)

    def rotate(self, matrix):
        """ Applies matrix tranformation to atom coordinates """
        self.x,self.y,self.z = trans([self.x,self.y,self.z],matrix)

#------------------------------------------------------------------------------

class Coordinates:
    """ Class describing a coordinates file in CHARMM or PDB format"""

    def __init__ (self,filename=None):
        self.filename = filename
        self.format = "" #Input format: pdb or charmm
        self.atoms = []  #List of atoms instances
        self.lines = []  #Line type: coordinates or remarks


    def readpdb (self,filename):
        """ Very basic parser reading only coordinates lines"""

        #Regex for coordinates line
        regex = re.compile("^(HETATM)|(ATOM)")

        try:
            filin = open(filename,"r")
        except IOError as e:
            print("I/O error({0}): {1}".format(e.errno, e.strerror))
            exit()

        for line in filin:
            if regex.match(line):
                atom = Atom()
                if self.atoms:
                    atom.setpdb(line, self.atoms[-1].num)
                else:
                    atom.setpdb(line)
                self.atoms.append(atom)
                self.lines.append("ATOM")
            else:
                self.lines.append(line.rstrip())
        filin.close()

    def readcrd (self,filename):
        """ Basic parser reading only coordinates lines"""

        #Regex for coordinates line
        regex = re.compile("^ *([0-9]+\s+){2}([A-Za-z0-9]+\s+){2}\
        ([\d\.e-]+\s+){3}[A-Za-z0-9]+\s+[0-9]+\s+[\d\.-]+")

        try:
            filin = open(filename,"r")
        except IOError as e:
            print("I/O error({0}): {1}".format(e.errno, e.strerror))
            exit()

        for line in filin:
            if regex.match(line):
                atom = Atom()
                atom.setcrd(line)
                self.atoms.append(atom)
                self.lines.append("ATOM")
            else:
                self.lines.append(line.rstrip())
        filin.close()

    def writepdb(self,filename):
        re_crd = re.compile("^[\* ]")        

        filout = open(filename,"w")
        c = 0
        for i in range(len(self.lines)):
            if self.lines[i] == "ATOM":
                filout.write(self.atoms[c].pdb_format())
                c += 1
            elif re_crd.match(self.lines[i]):
                filout.write("REMARK"+self.lines[i]+"\n")
            else:
                filout.write(self.lines[i]+"\n")
        filout.close()

    def writecrd(self,filename):
        filout = open(filename,"w")
        c = 0
        if self.format == 'pdb':
            filout.write("%10d  EXT\n" % len(self.atoms))
        for i in range(len(self.lines)):
            if self.lines[i] == "ATOM":
                filout.write(self.atoms[c].crd_format())
                c += 1
            elif self.format != 'pdb':
                filout.write(self.lines[i]+"\n")
        filout.close()

    def rotate_atoms(self, matrix):
        """ Applies matrix tranformation to atom coordinates """
        for atom in self.atoms:
            atom.rotate(matrix)    

#------------------------------------------------------------------------------
      
class Cell:
    """ Class describing unit cell parameters of xsc file"""
    def __init__(self,xscfile=None):
        self.step = None     #Time step
        self.a_vector = None # 1st cell vector
        self.b_vector = None # 2nd cell vector
        self.c_vector = None # 3rd cell vector
        self.ori = None      # Origin coordinates
        self.s_vector = None # If langevin on
        self.norm = None     # Vectors norm

        if xscfile:
            self.read(xscfile) 

    def read(self,xscfile):
        """ Read stream file and checks values"""
        try:
            filin = open(xscfile,"r")
        except IOError as e:
            print("I/O error({0}): {1}".format(e.errno, e.strerror))
            exit()

        regex = re.compile("([\d\.e-]+\s+){13,19}")
        self.step = 0
        abc = []
        for line in filin:
            sline = line.strip()
            if line.startswith(" SET A "):
                abc.append(float(sline.split(' = ')[1]))
            if line.startswith(" SET B "):
                abc.append(float(sline.split(' = ')[1]))
            if line.startswith(" SET C "):
                abc.append(float(sline.split(' = ')[1]))

        if sum(abc) / 3. != abc[0]:
            print("ERROR! Angles (%.5f,%.5f,%.5f) not equal to %.5f degrees"\
                % (a1, a2, a3, angle))
            exit()

        b = abc[0] / (3 * np.sqrt(3))
        b5 = b * 5
        self.a_vector = np.array([b5, -b, -b])
        self.b_vector = np.array([-b, b5, -b])
        self.c_vector = np.array([-b, -b, b5])
        self.ori = np.array([0.0, 0.0, 0.0])        
        filin.close()


    def check_cell(self):    
        # File format        
        if None in [x for x in [self.step, self.a_vector, self.b_vector, self.c_vector,\
                    self.ori] if type(x) == type(None)]:
            print("Format error! Check xsc file format")
            exit()

        # Norms
        if round(np.linalg.norm(self.a_vector),10) == \
        round(np.linalg.norm(self.b_vector),10) == \
        round(np.linalg.norm(self.c_vector),10):
            self.norm = np.linalg.norm(self.a_vector)
        else :
            print("ERROR! The norms of three vectors are not the same %.20f %.20f %.20f" \
                % (np.linalg.norm(self.a_vector), np.linalg.norm(self.b_vector)\
                ,np.linalg.norm(self.c_vector)))
            exit()

        # Angles    
        angle = 1.91063 #angle between vectors
        a1 = round(angle_between(self.a_vector,self.b_vector),5)
        a2 = round(angle_between(self.b_vector,self.c_vector),5)
        a3 = round(angle_between(self.a_vector, self.c_vector),5)        
        if not ((a1 == a2 == a3) and (round(a1,5) == angle)):
            print("ERROR! Angles (%.5f,%.5f,%.5f) not equal to %.5f degrees"\
                % (a1, a2, a3, angle))
            exit()

    def write(self,filename):
        filout = open(filename,"w")    
        filout.write("# NAMD extended system trajectory file\n")
        # Langevin on
        if self.s_vector != None:
            filout.write("#$LABELS step a_x a_y a_z b_x b_y b_z c_x c_y c_z \
o_x o_y o_z s_x s_y s_z s_u s_v s_w\n")
            filout.write("%d %.10f %.10f %.10f %.10f %.10f %.10f %.10f %.10f \
%.10f %.10e %.10e %.10e %.10e %.10e %.10e %.10e %.10e %.10e\n"  % \
            (self.step, self.a_vector[0], self.a_vector[1], self.a_vector[2],\
            self.b_vector[0], self.b_vector[1], self.b_vector[2],\
            self.c_vector[0], self.c_vector[1], self.c_vector[2],\
            self.ori[0], self.ori[1], self.ori[2],\
            self.s_vector[0], self.s_vector[1],self.s_vector[2],\
            self.s_vector[3],self.s_vector[4],self.s_vector[5]))

        # Langevin off (no s_vector)
        else:
            filout.write("#$LABELS step a_x a_y a_z b_x b_y b_z c_x c_y c_z \
o_x o_y o_z\n")
            filout.write("%d %.10f %.10f %.10f %.10f %.10f %.10f %.10f %.10f \
%.10f %.10e %.10e %.10e\n"  % \
            (self.step, self.a_vector[0], self.a_vector[1], self.a_vector[2],\
            self.b_vector[0], self.b_vector[1], self.b_vector[2],\
            self.c_vector[0], self.c_vector[1], self.c_vector[2],\
            self.ori[0], self.ori[1], self.ori[2]))

    def namd_norm(self):
        """
        Returns cell instance aligned with X-axis.
        Output vectors:
        v1:     d            0            0
        v2: -1/3d  2/3sqrt(2)d            0    
        v3: -1/3d -1/3sqrt(2)d -1/3sqrt(6)d
        """

        norm_cell = copy.copy(self)

        d1 = (-1./3)*self.norm
        d2 = (2./3)*np.sqrt(2)*self.norm
        d3 = (-1./3)*np.sqrt(2)*self.norm
        d4 = (-1./3)*np.sqrt(6)*self.norm    

        norm_cell.a_vector = np.array([self.norm,0,0])
        norm_cell.b_vector = np.array([d1,d2,0])
        norm_cell.c_vector = np.array([d1,d3,d4])

        return norm_cell

###############################################################################
# Functions
##############################

def unit_vector(vector):
    """ Returns the unit vector of the vector.  """

    return vector / np.linalg.norm(vector)


def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2' """

    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    angle = np.arccos(np.dot(v1_u, v2_u))

    if np.isnan(angle):
        if (v1_u == v2_u).all():
            return 0.0
        else:
            return np.pi
    return angle


def trans(p,m):
    """ Returns the transformed coordinates of p according to the matrix m"""

    return np.ravel(np.dot(p,m))


def rot_matrix(theta, axis):
    """
    Returns rotation matrix of theta around arounf a unit vector (x,y,z)

    M = I + sin(theta).Q + (1 - cos(theta)).Q^2

    with I : identity matrix
             /  0 -z  y  \
     and Q = |  z  0 -x  |
             \ -y  x  0  /
    """

    #Check if the vector norm = 1
    if np.linalg.norm(axis) != 1 :
        axis = unit_vector(axis)

    #Declare variables
    i = np.matrix(((1.,0.,0.),(0.,1.,0.),(0.,0.,1.)))
    q = np.matrix(((0.,-axis[2],axis[1]),(axis[2],0.,-axis[0]),(-axis[1],axis[0],0.)))

    #Compute rotation matrix
    m = i + np.dot(np.sin(theta),q) + np.dot((1 - np.cos(theta)),q**2)

    return np.matrix(m)


def define_rot(cell, cell_namd):
    """ Calculates the rotation matrix for superimposing cell to cell_namd"""    

    # Computes normalized bisector vector between both x vectors 
    bis_v = unit_vector(cell.a_vector + cell_namd.a_vector)    

    # 180 Degrees rotation matrix around this vector
    m1 = rot_matrix(np.pi, bis_v)

    # Rotates 2nd vector cell with m1 matrix
    v2_rot = trans(cell.b_vector,m1)    

    # Projects two 2nd vectors in zOy plane
    v2_rot_proj = (0., v2_rot[1],v2_rot[2])
    v2_namd_proj = (0., cell_namd.b_vector[1], cell_namd.b_vector[2])

    # Computes angle between 2nd vectors and rotation matrix around X-axis
    angle = angle_between(v2_rot_proj, v2_namd_proj)
    m2 = rot_matrix(angle, (1.,0.,0.))

    # Combines rotation matrices
    m3 = np.dot(m1,m2)

    return m3

def parseArg():
    """
    Gets all arguments
    """

    arguments=argparse.ArgumentParser(description="""This scripts modifies\
    NAMD xsc files to be constitent with the NAMD cell orientation convention\
    (ie aligned with X-axis) and performs a rotation of the corresponding pdb.""")
    arguments.add_argument('-p', "--pdb", help="pdb file")
    arguments.add_argument('-c', "--crd", help="CHARMM crd file",default = False)
    arguments.add_argument('-x', "--xsc", help="NAMD xsc file")
    arguments.add_argument('-o', '--output', help="output prefix. Default: rotated"\
    , default = "rotated")
    args = vars(arguments.parse_args())

    return(args)

###############################################################################
# MAIN
##############################

if __name__ == "__main__":

    # Gets arguments    
    myArgs=parseArg()
    pdbin = myArgs['pdb']
    xscin = myArgs['xsc']
    crdin = myArgs['crd']
    xscout = myArgs['output']+".xsc"
    pdbout = myArgs['output']+".pdb"
    crdout = myArgs['output']+".crd"

    # Reads files:
    xsc = Cell(xscin)
    xsc.check_cell()

    # Aligns cell with X-axis and computes rotation matrix
    xsc_namd = xsc.namd_norm()
    mat = define_rot(xsc,xsc_namd)  
    xsc_namd.write(xscout)

    # Rotates atoms and writes new pdb
    if pdbin :
        pdb = Coordinates()
        pdb.format = "pdb"
        pdb.readpdb(pdbin)
        pdb.rotate_atoms(mat)
        pdb.writepdb(pdbout)
        pdb.writecrd(crdout)

    # Rotates atoms and writes new pdb
    if crdin :
        crd = Coordinates()
        crd.format = "crd"
        crd.readcrd(crdin)
        crd.rotate_atoms(mat)
        crd.writecrd(crdout)
        crd.writepdb(pdbout)

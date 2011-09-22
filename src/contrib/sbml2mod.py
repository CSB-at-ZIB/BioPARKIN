#!/usr/bin/python
# sbml2mod.py

# Updated: 2/5/10

import sys,cStringIO,libsbml,traceback

__doc__="""sbml2mod version 3.1.1.1

Copyright (C) 2005-2010, Darren J Wilkinson
 d.j.wilkinson@ncl.ac.uk
 http://www.staff.ncl.ac.uk/d.j.wilkinson/

Includes modifications by:
  Jeremy Purvis (jep@thefoldingproblem.com)
  Carole Proctor (c.j.proctor@ncl.ac.uk)
  Mark Muldoon (m.muldoon@man.ac.uk)
  Lukas Endler (lukas@ebi.ac.uk)
 
This is GNU Free Software (General Public License)

Module for converting SBML to SBML-shorthand model files, version 3.1.1
Typical usage:
>>> from sbml2mod import Parser
>>> p=Parser(sbmldoc)
>>> p.parseStream(sys.stdout)

Raises error "ParseError" on a fatal parsing error.
"""

ParseError="Parsing error"


class Parser(object):
    """Parser class
Has constructor:
 Parser(sbmldoc)
where sbmldoc is a libsbml sbmldocument object,
and the following public methods:
 parseStream(outStream)
 parse()
"""

    def __init__(self,d):
        self.d=d
        self.m=d.getModel()

    def parseStream(self,outS):
        """parseStream(outStream)
parses SBML model and writes SBML-shorthand to outStream"""
        outS.write('@model:')
        outS.write(str(self.d.getLevel())+'.')
        outS.write(str(self.d.getVersion())+'.')
	self.mangle=10*self.d.getLevel()+self.d.getVersion()
        outS.write('0='+self.m.getId())
        if (self.m.getName()!=""):
            outS.write(' "'+self.m.getName()+'"')
        outS.write('\n')
        # level 3 global units...
        if (self.mangle>=30):
            first=True
            if self.m.isSetSubstanceUnits():
                if first==True:
                    outS.write(' ')
                    first=False
                else:
                    outS.write(',')
                outS.write('s='+str(self.m.getSubstanceUnits()))
            if self.m.isSetTimeUnits():
                if first==True:
                    outS.write(' ')
                    first=False
                else:
                    outS.write(',')
                outS.write('t='+str(self.m.getTimeUnits()))
            if self.m.isSetVolumeUnits():
                if first==True:
                    outS.write(' ')
                    first=False
                else:
                    outS.write(',')
                outS.write('v='+str(self.m.getVolumeUnits()))
            if self.m.isSetAreaUnits():
                if first==True:
                    outS.write(' ')
                    first=False
                else:
                    outS.write(',')
                outS.write('a='+str(self.m.getAreaUnits()))
            if self.m.isSetLengthUnits():
                if first==True:
                    outS.write(' ')
                    first=False
                else:
                    outS.write(',')
                outS.write('l='+str(self.m.getLengthUnits()))
            if self.m.isSetExtentUnits():
                if first==True:
                    outS.write(' ')
                    first=False
                else:
                    outS.write(',')
                outS.write('e='+str(self.m.getExtentUnits()))
            if self.m.isSetConversionFactor():
                if first==True:
                    outS.write(' ')
                    first=False
                else:
                    outS.write(',')
                outS.write('c='+str(self.m.getConversionFactor()))
            if (first==False):
                outS.write('\n')
        n=self.m.getNumUnitDefinitions()
        if (n>0):
            outS.write('@units\n')
            for i in range(n):
                ud=self.m.getUnitDefinition(i)
                outS.write(' '+ud.getId())
                for j in range(ud.getNumUnits()):
                    if (j==0):
                        outS.write('=')
                    else:
                        outS.write('; ')
                    u=ud.getUnit(j)
                    kind=u.getKind()
                    outS.write(libsbml.UnitKind_toString(kind))
                    e=u.getExponent()
                    m=u.getMultiplier()
                    o=u.getOffset()
                    s=u.getScale()
                    first=True
                    if (e!=1):
                        if first==True:
                            outS.write(':')
                            first=False
                        else:
                            outS.write(',')
                        outS.write('e='+str(e))
                    if (m!=1):
                        if first==True:
                            outS.write(':')
                            first=False
                        else:
                            outS.write(',')
                        outS.write('m='+str(m))
                    if (o!=0):
                        if first==True:
                            outS.write(':')
                            first=False
                        else:
                            outS.write(',')
                        outS.write('o='+str(o))
                    if (s!=0):
                        if first==True:
                            outS.write(':')
                            first=False
                        else:
                            outS.write(',')
                        outS.write('s='+str(s))
                if (ud.isSetName()):
                    outS.write(' "'+ud.getName()+'"')
                outS.write('\n')
        if self.m.getNumCompartments():
            outS.write('@compartments\n')
            for c in self.m.getListOfCompartments():
                outS.write(' '+c.getId())
                if (c.isSetOutside()):
                    outS.write('<'+c.getOutside())
                if (c.isSetSize()):
                    outS.write('='+str(c.getSize()))
                if (c.isSetName()):
                    outS.write(' "'+c.getName()+'"')
                outS.write('\n')
        if self.m.getNumSpecies():
            outS.write('@species\n')
            for s in self.m.getListOfSpecies():
                outS.write(' '+s.getCompartment()+':')
                if (s.isSetInitialConcentration()):
                    outS.write('['+s.getId()+']='+str(s.getInitialConcentration()))
                elif (s.isSetInitialAmount()):
                    outS.write(s.getId()+'='+str(s.getInitialAmount()))
                else:
                    outS.write('['+s.getId()+']='+str(s.getInitialConcentration()))
                if (s.getHasOnlySubstanceUnits()):
                    outS.write('s')
                if (s.getBoundaryCondition()):
                    outS.write('b')
                if (s.getConstant()):
                    outS.write('c')
                if (s.isSetName()):
                    outS.write(' "'+s.getName()+'"')
                outS.write('\n')
        if self.m.getNumParameters():
            outS.write('@parameters\n')
            for p in self.m.getListOfParameters():
                outS.write(' '+p.getId()+'=')
                outS.write(str(p.getValue()))
                c=p.getConstant()
                if(c!=1):
                    outS.write('v')
                if (p.isSetName()):
                    outS.write(' "'+p.getName()+'"')
                outS.write('\n')
        if self.m.getNumRules():
            outS.write('@rules\n')
            for r in self.m.getListOfRules():
                if (r.isAssignment()):
                    outS.write(' ' + r.getVariable() + ' = ' + r.getFormula())
                    outS.write('\n')
                elif (r.isRate()):
                    outS.write(' @rate:' + r.getVariable() + ' = ' + r.getFormula())
                    outS.write('\n')
                else:
                    # probably an algebraic rule!
                    sys.stderr.write("Unsupported rule type\n")
                    raise(ParseError)
        if self.m.getNumReactions():
            outS.write('@reactions\n')
            for r in self.m.getListOfReactions():
                if (r.getReversible()):
                    outS.write('@rr=')
                else:
                    outS.write('@r=')
                outS.write(r.getId())
                if (r.isSetName()):
                    outS.write(' "'+r.getName()+'"')
                outS.write('\n ')
                for j in range(r.getNumReactants()):
                    sr=r.getReactant(j)
                    if (j>0):
                        outS.write('+')
                    sto=sr.getStoichiometry()
                    if (sto!=1):
                        outS.write(str(int(sto)))
                    outS.write(sr.getSpecies())
                outS.write(' -> ')
                for j in range(r.getNumProducts()):
                    sr=r.getProduct(j)
                    if (j>0):
                        outS.write('+')
                    sto=sr.getStoichiometry()
                    if (sto!=1):
                        outS.write(str(int(sto)))
                    outS.write(sr.getSpecies())
                for j in range(r.getNumModifiers()):
                    sr=r.getModifier(j)
                    if (j==0):
                        outS.write(' : ')
                        outS.write(sr.getSpecies())
                    else:
                        outS.write(', ')
                        outS.write(sr.getSpecies())
                outS.write('\n')
                if (r.isSetKineticLaw()):
                    kl=r.getKineticLaw()
                    outS.write(' '+kl.getFormula())
                    for k in range(kl.getNumParameters()):
                        if (k==0):
                            outS.write(' : ')
                        else:
                            outS.write(', ')
                        p=kl.getParameter(k)
                        outS.write(p.getId()+'='+str(p.getValue()))
                    outS.write('\n')
        if self.m.getNumEvents():
            outS.write('@events\n')
            for e in self.m.getListOfEvents():
                outS.write(" "+e.getId()+"= ")
                trig=e.getTrigger()
                trigger=libsbml.formulaToString(trig.getMath())
                outS.write(trigger)
                if e.isSetDelay():
                    outS.write(' ; ')
                    dmath=e.getDelay()
                    delay=libsbml.formulaToString(dmath.getMath())
                    outS.write(delay)
                outS.write(' : ')
                nea=e.getNumEventAssignments()
                for eai in range(nea):
                    if (eai>0):
		    	if (self.mangle>=23):
			    outS.write('; ')
			else:
                            outS.write(', ')
                    ea=e.getEventAssignment(eai)
                    outS.write(ea.getVariable()+"=")
                    m=ea.getMath()
                    mf=libsbml.formulaToString(m)
                    outS.write(mf)
                if e.isSetName():
                    outS.write(' "'+e.getName()+'"')
                outS.write("\n")


    def parse(self):
        """parse()
Parses the SBML model and returns a string containing the
corresponding SBML-shorthand"""
        outS=cStringIO.StringIO()
        self.parseStream(outS)
        return outS.getvalue()


if __name__=='__main__':
    argc=len(sys.argv)
    try:
        if (argc==1):
            s=sys.stdin
        else:
            try:
                s=open(sys.argv[1],"r")
            except:
                sys.stderr.write('Error: failed to open file: ')
                sys.stderr.write(sys.argv[1]+'\n')
                sys.exit(1)
        string=s.read()
        r=libsbml.SBMLReader()
        d=r.readSBMLFromString(string)
        # print d
        p=Parser(d)
        p.parseStream(sys.stdout)
    except:
        traceback.print_exc(file=sys.stderr)
        sys.stderr.write('\n\n Unknown parsing error!\n')
        sys.exit(1)


# eof


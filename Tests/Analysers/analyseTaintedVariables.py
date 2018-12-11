#    Copyright (C) 2018 Rajeev Gopalakrishna
#
#    This file is part of Solstice.
#
#    Solstice is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    Solstice is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import unittest
import subprocess, os, sys
from ParseAST.parseAST import ParseAST
from Analysers.mapASTSourceToLineNumbers import MapASTSourceToLineNumbers
from Analysers.analyseTaintedVariables import AnalyseTaintedVariables

class TestTaintedVariables(unittest.TestCase):

    testFile = "taintedVariables"
    testDir = "./Tests/Analysers/"
    testPath = testDir+testFile

    def setUp(self):
        astFD = open(self.testPath+".ast","w")
        errFD = open(self.testPath+".err","w")
        p = subprocess.Popen(['solc','--ast-compact-json',self.testDir+'Contracts/'+self.testFile+'.sol'], stdout=astFD,stderr=errFD)
        p.wait()
        astFD.close()
        errFD.close()

    def tearDown(self):
        p = subprocess.Popen(['rm','-f',self.testPath+'.ast',self.testPath+'.err'])
        p.wait()
        
    def test_exceptions(self):
        parseAST = ParseAST()
        astFD = open(self.testPath+".ast","r")
        parseResults = parseAST.parse(astFD)
        mapASTSourceToLineNumbers = MapASTSourceToLineNumbers()
        mapASTSourceToLineNumbers.analyser(self.testDir+"Contracts/"+self.testFile+".sol")
        analyseTaintedVariables = AnalyseTaintedVariables()
        analyseTaintedVariables.analyser()
        self.assertEqual(len(analyseTaintedVariables.statsTaintedVariables), 6)
        self.assertEqual(len(analyseTaintedVariables.statsTaintedVariables[0]["info"]), 1)
        self.assertEqual(len(analyseTaintedVariables.statsTaintedVariables[1]["info"]), 2)
        self.assertEqual(len(analyseTaintedVariables.statsTaintedVariables[2]["info"]), 3)
        self.assertEqual(len(analyseTaintedVariables.statsTaintedVariables[3]["info"]), 3)
        self.assertEqual(len(analyseTaintedVariables.statsTaintedVariables[4]["info"]), 4)
        self.assertEqual(len(analyseTaintedVariables.statsTaintedVariables[5]["info"]), 5)
        astFD.close()
        
if __name__ == '__main__':
    unittest.main()

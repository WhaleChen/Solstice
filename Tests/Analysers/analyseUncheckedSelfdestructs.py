#	Copyright (c) 2018 Rajeev Gopalakrishna
#
#	This file is part of Solstice.
#
#	Solstice is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	Solstice is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with Solstice.  If not, see <http://www.gnu.org/licenses/>.

import unittest
import subprocess, os, sys
from ParseAST.parseAST import ParseAST
from Analysers.mapASTSourceToLineNumbers import MapASTSourceToLineNumbers
from Analysers.analyseUncheckedSelfdestructs import AnalyseUncheckedSelfdestructs

class TestUncheckedSelfdestructs(unittest.TestCase):

    testFile = "uncheckedSelfdestructs"
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
        analyseUncheckedSelfdestructs = AnalyseUncheckedSelfdestructs()
        analyseUncheckedSelfdestructs.analyser()
        self.assertEqual(len(analyseUncheckedSelfdestructs.statsConditionalCheckedSelfdestructs), 1)
        self.assertEqual(analyseUncheckedSelfdestructs.statsConditionalCheckedSelfdestructs[0]["line"], "13")
        self.assertEqual(len(analyseUncheckedSelfdestructs.statsUncheckedSelfdestructs), 1)
        self.assertEqual(analyseUncheckedSelfdestructs.statsUncheckedSelfdestructs[0]["line"], "17")
        astFD.close()
        
if __name__ == '__main__':
    unittest.main()
from django.test import TestCase
import form_table
import datetime
import time


# Create your tests here.


class TabelesTestCase(TestCase):
    def setUp(self) -> None: 
        self.test_table1= {
                    1703160000 :[1],
                    1703073600 :[1],
                    1702987200 :[1],
                    1702900800 :[1],
                    1702814400 :[1],
                    1702814400 :[1],
                    1702728000 :[1],
                    1702641600 :[1],
                    1702555200 :[1],
                    1702468800 :[1],
                    1702382400 :[1],
                    1702296000 :[1],
                    1702209600 :[1],
                    1702123200 :[1],
                    1702036800 :[1],
                    1701950400 :[1],
                    1701864000 :[1],
                    1701777600 :[1],
                    1701691200 :[1],
                    1701604800 :[1],
                    1701518400 :[1],
                    1701432000 :[1],
                    1701345600 :[1],
                    1701259200 :[1],
                    1701172800 :[1],
                    1701086400 :[1],
                    1701000000 :[1],
                    1700913600 :[1],
                    1700827200 :[1],
                    1700740800 :[1],
                    1700654400 :[1],
                    1700568000 :[1],
                    1700481600 :[1],
                    1700395200 :[1],
                    1700308800 :[1],
                    1700222400 :[1],
                    1700136000 :[1],
                    1700049600 :[1],
                    1699963200 :[1]
                }

    def test_table_merge(self):
        self.test_table2= {} 
        # self.test_table3 = self.test_table1.copy()
        self.assertEqual(form_table.merge_data(self.test_table2,self.test_table1), self.test_table1)
        # self.test_table1 = self.test_table3.copy()

    def test_table_merge_errors(self):
        with self.assertRaises(TypeError):
            data = form_table.merge_data(self.test_table1,self.test_table1)

import unittest
import sys
import os
import time
import threading

class EmailTestRunner(unittest.TextTestRunner):

	def __init__(self):
		super(EmailTestRunner, self).__init__()
		self.suite = EmailTestSuite()
		self.verbosity = 2

    # overridden method
	def run(self):
		return super(EmailTestRunner, self).run(self.suite)


class EmailTestSuite(unittest.TestSuite):

	def __init__(self):
		super(EmailTestSuite, self).__init__()
		self.loader = unittest.TestLoader()
		self.load_tests()

		return

	def load_tests(self):

		# find all test files in directory
		tests_directory = os.path.abspath(os.path.dirname(__file__))
		test_modules = [
			filename.replace('.py','')
			for filename in os.listdir(tests_directory)
			if filename.endswith('tests.py') and not filename.startswith('run')
		]
		map(__import__,test_modules)

		# load tests
		for module in [sys.modules[modname] for modname in test_modules]:
			self.addTests(self.loader.loadTestsFromModule(module))

if __name__=='__main__':
	test_runner  = EmailTestRunner()
	results      = test_runner.run()

	# count errors and failures
	tests_failed = len(results.errors) + len(results.failures)

	# return code to runner
	# 0 = success, 1 = failure
	# the script can be then directly plugged into continuous integration tools
	sys.exit((1 if tests_failed > 0 else 0))
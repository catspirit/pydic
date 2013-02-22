# Work around mbcs bug in distutils.
# http://bugs.python.org/issue10945
if 1: # disable when fixed
    import codecs
    try:
        codecs.lookup('mbcs')
    except LookupError:
        ascii = codecs.lookup('ascii')
        func = lambda name, enc=ascii: {True: enc}.get(name=='mbcs')
        codecs.register(func)

from distutils.core import setup

setup(name='education dictionary',
      version='1.0',
      author='Chenhui Yin',
      author_email='chenhui.yin@email.wsu.edu',
      packages=['src_edt','src_eds'],
      package_dir = {'': 'src'},
      py_modules=['run_teacher','run_student']
      )

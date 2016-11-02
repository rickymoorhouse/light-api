# setup.py
""" Installation for pilight """
from setuptools import setup, find_packages

setup(
    name='pilight',
    version='1.0',

    description='Abstraction layer for Raspberry pi lights',

    author='Ricky Moorhouse',
    author_email='ricky@samespirit.net',

    url='http://github.com/rickymoorhouse',

    classifiers=['Development Status :: 3 - Alpha',
                 'License :: OSI Approved :: Apache Software License',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.7',
                 'Intended Audience :: Developers',
                 'Environment :: Console',
                ],

    platforms=['Any'],

    scripts=[],

    provides=['pilight',
             ],

    packages=find_packages(),
    include_package_data=True,
    install_requires=["stevedore", "cherrypy"],
    test_requires=["nose", "mock"],
    entry_points={
        'console_scripts': ['pilight=pilight:start_server'],
        'pilight.device': [
            'unicornhat = pilight.unicorn_hat:Unicorn',
            'console = pilight.text:Text',
            'piglow = pilight.pi_glow:PiGlow',
        ],
    },

    zip_safe=False,
)

from distutils.core import setup
 
setup(
    name='pyplex',
    version='0.1.0',
    author='Dale Hamel',
    author_email='dale.hamel@srvthe.net',
    packages=['pyplex', 'pyplex.plexapi',   'pyplex.xbmc', 'pyplex.gui', 'pyplex.omxplayer',  'pyplex.zeroconf','pyplex.core'],
    package_dir={'pyplex':'pyplex'},
    package_data={'pyplex':['images/logo.png']},
    scripts=['scripts/pyplex'],  # don't forget to add a script
    url='https://pip.srvthe.net/sample/pyplex',
    license='LICENSE.txt',
    description='Plex frontend playback service controllable by iOS and Adroid app',
    install_requires=[
        "twisted",
        "twisted-web",
        "pexpect",
        "requests",
        "pygame"
    ],
)

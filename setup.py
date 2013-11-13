from setuptools import setup, find_packages

setup(
    name='django-vkontakte-users',
    version=__import__('vkontakte_users').__version__,
    description='Django implementation for vkontakte API Users',
    long_description=open('README.md').read(),
    author='ramusus',
    author_email='ramusus@gmail.com',
    url='https://github.com/ramusus/django-vkontakte-users',
    download_url='http://pypi.python.org/pypi/django-vkontakte-users',
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False, # because we're including media that Django needs
    install_requires=[
        'python-dateutil==1.5',
        'django-vkontakte-api>=0.4.5',
        'django-vkontakte-places>=0.3.0',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)

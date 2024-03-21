from distutils.core import setup

setup(
    name='chatpdf_master',  # How you named your package folder (foo)
    packages=['chatpdf_master'],  # Chose the same as "name"
    version='0.1',  # Start with a small number and increase it with every change you make
    license='MIT',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description='Efficient access to chatpdf models',  # Give a short description about your library
    author='ZhangXiaobo',  # Type in your name
    author_email='1735824639@qq.com',  # Type in your E-Mail
    url='https://github.com/xiaoboQ/chatpdf_master',  # Provide either the link to your github or to your website
    download_url='https://github.com/xiaoboQ/chatpdf_master/archive/master.zip',
    keywords=['LLM', 'chatpdf'],  # Keywords that define your package best
    install_requires=['requests'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',  # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',  # Again, pick a license
        'Programming Language :: Python :: 3',  # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)

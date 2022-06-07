from setuptools import setup    # type: ignore

with open('./README.md', encoding='utf8') as file_obj:
    long_description = file_obj.read()

with open('./requirements.txt', encoding='utf8') as file_obj:
    requirements = file_obj.readlines()

setup(
    name='ycfunc',
    version='0.0.1',
    license='MIT',
    description='Yandex Cloud functions wrapper',
    long_description=long_description,
    packages=['ycfunc'],
    install_requires=requirements,
    python_requires='>=3.6',
)

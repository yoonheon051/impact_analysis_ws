import os
from glob import glob
from setuptools import setup

package_name = 'dsr_impact_analysis'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'urdf'), glob('urdf/*')),
        # meshes 폴더 안의 '파일'들만 깔끔하게 복사
        (os.path.join('share', package_name, 'meshes'), glob('meshes/*')),
    ],

    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='rokey',
    maintainer_email='rokey@todo.todo',
    description='M0609 Impact Analysis Project',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'impact_sim_node = dsr_impact_analysis.impact_sim_node:main'
        ],
    },
)

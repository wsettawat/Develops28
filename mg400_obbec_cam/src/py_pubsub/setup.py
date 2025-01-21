from setuptools import find_packages, setup

package_name = 'py_pubsub'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='wedo2',
    maintainer_email='settawaw@scg.com',
    description='TODO: Package description',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'talker = py_pubsub.publisher_member_function:main',
            'listener = py_pubsub.subscriber_member_function:main',
            'seg = py_pubsub.segmentation_pic_rgb_01:main',
            'sync = py_pubsub.sync_image:main',
            'seg1 = py_pubsub.segment_depth_rgp_01:main',
            'repoint = py_pubsub.republish_point:main',
        ],
    },
)

from setuptools import setup, find_packages


setup(name='mobiface',
      version='0.0.1',
      description='MobiFace benchmark official API',
      author='Yiming Lin',
      author_email='mobiface.ibug@gmail.com',
      license='MIT',
      install_requires=[
          'numpy', 'matplotlib', 'Pillow', 'Shapely', 'fire', 'tqdm', 'pandas'],
      packages=find_packages(),
      include_package_data=True,
      )

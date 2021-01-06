import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ryzetello",                                                  
    version="1.6",                                                          
    author="Gabriel Heinzer",                                               
    author_email="dev@gabrielheinzer.ch",                                   
    description="This simple Library should help you controlling the TELLO EDU over WiFi with Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/programmer372/python-tello",             
    packages=setuptools.find_packages(),
    #classifiers=[
        #"Programming Language :: Python :: 3",                              
        #"License :: OSI Approved :: MIT License",
        #"Operating System :: OS Independent",
    #],
    python_requires=">=3.6",                                                
    include_package_data=True
)

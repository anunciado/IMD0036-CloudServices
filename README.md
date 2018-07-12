# Cloud Services

In this project we implemented a cloud services server capable of processing images. Our server will perform tasks for the client, while the client does other (or no) tasks.

### Prerequisites

You will need to install the modules below to run the program: 
* [python 3.7 or greater](https://www.python.org/downloads/release/python-370/)
* [zmq](https://pypi.org/project/zmq/)
* [cv2](https://pypi.org/project/opencv-python/)

### Running

There are two ways to run the program:

* Compile the IDE (PyCharm - Python IDE):
1. Just open the IDE
2. Import the project folder as a Project
3. Select Run/Debug Configurations:
For server:
```
-a <alphafile> -p <port>
```
An example would be:
```
-a ../input/pelican.png -p 9000
```
For client:
```
-i <inputfile> -o <outputfile> -p <port> -t <technique>
```
An example would be:
```
-i ../input/luis.png -o ../output/process_image.png -p 9000 -t alpha
```
4. Choose Run client on the context menu.
5. Choose Run server on the context menu.
6. From this it only interacts with the system and add in script parameters box contents:

* Compile by terminal:
1. Enter the src folder and run the following command:
For server:
```
$ python server.py -a <alphafile> -p <port>
```
An example would be:
```
$ python server.py -a ../input/pelican.png -p 9000
```
For client:
```
$ python client.py -i <inputfile> -o <outputfile> -p <port> -t <technique>
```
An example would be:
```
$ python client.py -i ../input/luis.png -o ../output/process_image.png -p 9000 -t alpha
```
2. From this it only interacts with the system.

## Built With

* [PyCharm](https://www.jetbrains.com/pycharm/) - A IDE used

## Authors
### Developers: 
* **Luís Eduardo Anunciado Silva ([cruxiu@ufrn.edu.br](mailto:cruxiu@ufrn.edu.br))** 
* **Larissa Gilliane Melo De Moura ([larissagilliane@ufrn.edu.br](mailto:larissagilliane@ufrn.edu.br))** 
### Project Advisor: 
* **Julio Cesar Paulino De Melo ([julio.melo@imd.ufrn.br](mailto:julio.melo@imd.ufrn.br))** 

See also the list of [contributors](https://github.com/cruxiu/IMD0036-CloudServices/contributors) who participated in this project.

## License

This project is licensed under the GPL 3.0 - see the [LICENSE](LICENSE) file for details

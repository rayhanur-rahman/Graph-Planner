1. the programs are all written in python 3. So, you need to install python version 3 on your system. For Debian based Linux, you can install it by this command: sudo apt install python3
2. There is three python files: App.py, Node.py and Utils.py. You only need to run App.py
3. The command to run the code is: python3 App.py <traindata> <testdata> <class> <criteria>
4. traindata and testdata are the csv files for training and testing datasets
5. class will be the name of the column you are trying to predict
6. criteria will be either 0 or 1. 0 for infogai and 1 for the alternative
7. one complete command is like this: python3 App.py SpectHeart_train.csv SpectHeart_test.csv class 0
8. the output will be like this: {'true positive': 39, 'true negative': 4, 'false positive': 7, 'false negative': 4, 'accuracy': 0.7962961488340464, 'precision': 0.8478259026465429, 'recall': 0.9069765332612713, 'f-measure': 0.8763993031467956}
9. in the treeouput.txt, the tree will be printed. 


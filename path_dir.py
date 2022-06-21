server=0
if server==0:
    path='E:\Tom_Utopia\Accounting\\'
    sep='\\'
elif server==1:
    #this is for Mac
    path='/volume1/Python/ASM/product/'
    sep='/'
    path_data='/volume1/Python/ASM/product/data/'
#lok fu pc as 2
elif server==2:
    path='C:\polygon\\'
    sep='\\'
    path_data='C:\polygon\data\\'

if __name__=='__main__':
    print (f'{path_data}test.csv')
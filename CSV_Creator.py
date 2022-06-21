import pandas as pd
import numpy as np
import os.path
from path_dir import path,sep

def new_csv(name,folder,column_array):
    print('Here comes the creating new csv program...')
    df=pd.DataFrame(list(),columns=column_array)

    print(df)
    df.to_csv(f'{path}{folder}\{name}.csv',index=False)
    print(f'{name}.csv is created',df.columns)

# name = Software, folder, T: a=C+L+Reveune-Expense
def add_data(name,folder):
    print("Here goes Add to Financial_Analysis Progress...")
    if os.path.exists(f'{path}{folder}'):
        print('Folder exists')
        df = pd.read_csv (f'{path}{folder}{sep}{name}.csv')
        new_df=pd.DataFrame(df)
        array=[]
        column=[]
        for i in range(len(df.columns)):
            column.append(df.columns[i])
            print('Data for ',df.columns[i])
            newdata=input(':')
            array.append(newdata)

        print('This is the passing data array: ',array)
        print('This is the passing column array: ',column)
        df2=pd.DataFrame(np.array([array]),columns=column)

        new_df=new_df.append(df2)
        print(new_df)
        # print (new_stock_array)
        new_df.to_csv (f'{path}{folder}{sep}{name}.csv',index=False)

def add_multi_data(name,folder):
    print("Here goes Add multi data to Financial_Analysis Progress...")
    if os.path.exists(f'E:\Stock\ASM API Trading\data\{folder}'):
        print('Folder exists')
        df = pd.read_csv (f'E:\Stock\ASM API Trading\data\{folder}\{name}.csv')
        new_df=pd.DataFrame(df)
        
        nos_of_row=int(input('How many sets of data to be input:'))
        for j in range(nos_of_row):
            array=[]
            for i in range(len(df.columns)):
    
                print(f'[{j}] Data for',df.columns[i])
                newdata=input(':')
                array.append(newdata)
            df2=pd.DataFrame(np.array([array]),columns=df.columns)
            new_df=new_df.append(df2)

        new_df.to_csv (f'E:\Stock\ASM API Trading\data\{folder}\{name}.csv',index=False)


    else:
        print('Folder does not exist')



if __name__ == '__main__':
    while True:
        try:
            print('Welcome to CSV Creator programe!')
            choice=input('0:Create a new profile\n1:Add single data\n2:Add multi data\nYour input:')

            if choice=='0':
                print('A new profile will be created...')
                name=input('What is the name of the CSV you would like to create?')
                folder=input('What is the folder name of the CSV being put in?')
                if os.path.exists(f'E:\Tom_Utopia\Accounting\{folder}'):
                    print('Folder exists')
                    nos_column=int(input('How many Columes are in the CSV?'))
                    column_array=[]
                    for i in range(nos_column):
                        column_name=input(f'What is the name for Column {i}: ')
                        column_array.append(column_name)
                    new_csv(name,folder,column_array)
                else:
                    print('Folder not exists!')
            elif choice=='1':
                print('Here goes adding data to existing profile program...')
                name=input('What is the name of the CSV which data is to be added?')
                folder=input('What is the folder name of the CSV being edited?')
                add_data(name,folder)


            elif choice=='2':
                print('Here goes adding multi data to existing profile program...')
                name=input('What is the name of the CSV which data is to be added?')
                folder=input('What is the folder name of the CSV being edited?')
                add_multi_data(name,folder)

            elif choice=='8':

                new_csv(name,folder,column_array)

            else:
                print('Your input is invalid!')

        except KeyboardInterrupt:
            break
        
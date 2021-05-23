import insert
import query

# ASKS THE USER
def select_option():
    print('Choose option:')
    print('1) Drop DB & load data')
    print('2) Represent data')
    print('3) Exit')

    option = int(input())
    print('')

    if option==1: insert.load_data_selected()
    elif option==2: query.main()
    elif option==3: return

    else:
        print('\nSelect valid number\n')
        
    print("\n##############################\n")
    select_option()


# INFO & START
def run():
    print("\n##############################")
    print("REData with MongoDB")
    print("##############################\n\n")

    select_option()

run()


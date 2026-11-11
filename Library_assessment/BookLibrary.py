import csv

def load_and_search_library():
    file_name= "Library.csv"
    books_data = []
    try:

        with open(file_name,'r',newline='',encoding='utf-8')as file:
            reader=csv.DictReader(file)
            for row  in reader:
                books_data.append(row)
    except FileNotFoundError:
        print(f" eerror:{file_name} is not found.") 
        return
        
    while True :
        print("\n---------------------------------------------------------")
        print("1.Library Search system")
        print("2.list of Multiple Libraries and Books ")
        print("3.Search books with the name of Library ")
        print("4.Exit")
        print("-----------------------------------------------------------")
        choice = input("select option :").strip()
        if choice == '1':
            print(f"\n {'Library_Name'}|{'Book Title':<25}|{'Author':<20}|{'Status':<12}")
            print(" -" *60)
            #print(f"\n {book['Library_Name']:<20}|{book['Book Title']:<25}|{book['Author']:<20}|{book['Status']:<12}")
            for book in books_data:
                lib_name = book.get('Library_Name') or book.get('Library Name') or ""
                b_title = book.get('Book_Title') or book.get('Book Title') or ""
                b_author = book.get('Author') or ""
                b_status = book.get('Status') or ""
                print(f"{lib_name:<20} | {b_title:<25} | {b_author:<20} | {b_status:<12}")

        # Option-2: see list of books related to the particular library
        elif choice == '2':
            search_lib =input("write Library_name:").strip().lower()
            print(f"\n -- result for library: '{search_lib}'---")
            print(f" {'Book Title':<25}|{'Author':<20}|{'Status':<12}")
            print("_" *60)
            found = False
            
            for book in books_data:
                lib_name = str(book.get('Library_Name') or book.get('Library Name') or "").lower()
                if search_lib in lib_name:
                    b_title = book.get('Book_Title') or book.get('Book Title') or ""
                    b_author = book.get('Author') or ""
                    b_status = book.get('Status') or ""
                    print(f"{b_title:<25} | {b_author:<20} | {b_status:<12}")
                    found = True
                
            if not found :
                print(" There is no data related to the Library got")


        elif choice == '3':
            search_query = input("Write Name of Book or author :").strip().lower()
            print(f"\n--- Search Results for: '{search_query}' ---")
            print(f"{'Library Name':<20} | {'Book Title':<25} | {'Author':<20} | {'Status':<12}")
            print("-" * 60)
            found = False
            for book in books_data:
                # str(book.get(...) or "") NoneType_error will be rectified
                title = str(book.get('Book_Title') or book.get('Book Title') or "").lower()
                author = str(book.get('Author') or "").lower()
                if search_query in title or search_query in author:
                    lib_name = book.get('Library_Name') or book.get('Library Name') or ""
                    b_title = book.get('Book_Title') or book.get('Book Title') or ""
                    b_author = book.get('Author') or ""
                    b_status = book.get('Status') or ""
                    print(f"{lib_name:<20} | {b_title:<25} | {b_author:<20} | {b_status:<12}")
                    found = True
                           
            if  not found :
                print("There  is no Book or Author got.")
                
        elif choice =='4':
            print("\n Thanks for using of Library System..")
            break
        else :
            print("Option is wrong,Please select option betweeen 1 to 4")

if __name__== "__main__": 

    load_and_search_library()
            
        
            
                    
        
            
             
   

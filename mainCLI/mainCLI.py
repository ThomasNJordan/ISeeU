print("Initializing ICU...")
print(r"""
                   ___           ___     
    ___          /  /\         /__/\    
   /  /\        /  /:/         \  \:\   
  /  /:/       /  /:/           \  \:\  
 /__/::\      /  /:/  ___   ___  \  \:\ 
 \__\/\:\__  /__/:/  /  /\ /__/\  \__\:\
    \  \:\/\ \  \:\ /  /:/ \  \:\ /  /:/
     \__\::/  \  \:\  /:/   \  \:\  /:/ 
     /__/:/    \  \:\/:/     \  \:\/:/  
     \__\/      \  \::/       \  \::/   
                 \__\/         \__\/    
    
""")

print("What do you want to do (Type Number for Option):\n")                            
print("1. Start Motion Detection")
print("2. Enumerate Envrionment")
print("0. Exit\n")

user_input = input()

try:
    user_input = int(user_input)
except ValueError:
    user_input = None

match user_input:
    case 1:
        print("1. Beginning Capture")
            #Insert Code
    case 2:
        print("Environment Enumerating")
            #Insert Code
    case _:
        print("Default Reached")







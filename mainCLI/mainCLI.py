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

print("What do you want to do (Type # for Option):\n")                            
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
        print("1. Start with Capture")
        print("2. Display Only")
    case 2:
        print("Environment Enumerating")
    case _:
        print("Default Reached")







import colorama

colorama.init()

success = colorama.Fore.GREEN
fail = colorama.Fore.RED
reset = colorama.Fore.RESET  

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args 

def is_valid_name(name):
    return name.isalpha()  

def is_valid_phone(phone):
    return phone.isdigit()  

def input_error(func):
    def wrapper(contacts, *args):
        try:
            if func.__name__ in ["add_contact", "change_contact"]:
                if not args or len(args[0]) < 2:
                    return f"{fail}Give me name and phone please. Example: add John 1234567890{reset}"

                name, phone = args[0]
                if not is_valid_name(name):
                    return f"{fail}Invalid name. Use only letters.{reset}"
                if not is_valid_phone(phone):
                    return f"{fail}Invalid phone number. Use only digits.{reset}"

            elif func.__name__ == "show_phone":
                if not args or len(args[0]) < 1:
                    return f"{fail}Give me a name to find the phone number.{reset}"

            return func(contacts, *args)
        
        except KeyError:
            return f"{fail}Contact not found.{reset}"
        except ValueError:
            return f"{fail}Invalid input. Please provide correct values.{reset}"
        except IndexError:
            return f"{fail}Missing arguments. Example: add John 1234567890{reset}"
        except Exception as e:
            return f"{fail}Unexpected error: {str(e)}{reset}"
        
    return wrapper

@input_error
def add_contact(contacts, args):
    name, phone = args
    contacts[name] = phone
    return f"{success}Contact {name} added.{reset}"

@input_error
def change_contact(contacts, args):
    name, phone = args
    if name not in contacts:
        raise KeyError("Contact not found")  
    contacts[name] = phone
    return f"{success}Contact {name} updated.{reset}"

@input_error
def show_phone(contacts, args):
    name = args[0]
    if name not in contacts:
        raise KeyError("Contact not found")
    return f"{success}Contact {name}: {contacts[name]}{reset}"

@input_error
def show_all(contacts):
    if not contacts:
        return f"{fail}No contacts added yet.{reset}"
    
    res = f"{success}All contacts:{reset}"
    for name, phone in contacts.items():
        res += f"\n - {name}: {phone}"
    return res

def main():
    contacts = {}
    print(f"\n{success}Hello! Welcome to the assistant bot!{reset}\n")
    
    while True:
        try:
            user_input = input("Enter a command: ").strip()
            if not user_input:
                print(f"{fail}Please enter a command.{reset}")
                continue

            command, args = parse_input(user_input)

            if command in ["close", "exit"]:
                print(f"{success}Good bye!{reset}")
                break
            
            elif command == "hello":
                print(f"{success}How can I help you?{reset}")
                
            elif command == "add":
                print(add_contact(contacts, args))
                
            elif command == "change":
                print(change_contact(contacts, args))

            elif command == "phone":
                print(show_phone(contacts, args))
                
            elif command == "all":
                print(show_all(contacts))
                
            else:
                print(f"{fail}Invalid command.{reset}")

        except KeyboardInterrupt:
            print(f"\n{fail}Program interrupted. Exiting...{reset}")
            break
        except Exception as e:
            print(f"{fail}Unexpected error: {str(e)}{reset}")

if __name__ == "__main__":
    main()

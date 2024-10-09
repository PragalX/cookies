import os
import time

def read_cookies(file_path):
    with open(file_path, 'r') as file:
        return file.readlines()

def write_cookies(file_path, cookies):
    with open(file_path, 'w') as file:
        file.writelines(cookies)

def change_cookie_expiry(cookies, current_year, new_year):
    updated_cookies = []
    changes = []

    for line in cookies:
        parts = line.split('\t')
        
        if len(parts) > 4:  # Ensuring the line contains enough parts
            domain, flag, path, secure, expiry = parts
            
            # Convert expiry to int and check the year
            try:
                expiry_time = int(expiry)
                expiry_date = time.localtime(expiry_time)
                
                if expiry_date.tm_year == current_year:
                    # Change the expiry year to the new year
                    new_expiry_time = time.mktime((new_year, expiry_date.tm_mon, expiry_date.tm_mday,
                                                    expiry_date.tm_hour, expiry_date.tm_min, 
                                                    expiry_date.tm_sec, expiry_date.tm_yday, 
                                                    expiry_date.tm_year, 0))
                    
                    updated_cookies.append('\t'.join([domain, flag, path, secure, str(int(new_expiry_time))]) + '\n')
                    changes.append(f'Changed: {expiry_time} (Year {current_year}) to {int(new_expiry_time)} (Year {new_year})')
                else:
                    updated_cookies.append(line)
            except ValueError:
                updated_cookies.append(line)  # In case the expiry is not an integer
                changes.append(f'No change: Invalid expiry format in line: {line.strip()}')
        else:
            updated_cookies.append(line)  # Keep the line as is if it doesn't match the expected format
    
    return updated_cookies, changes

def main():
    input_file = 'cookies.txt'  # Path to the input cookies file
    output_file = 'updated_cookies.txt'  # Path to save the updated cookies file
    current_year = 2024
    new_year = 2025

    if not os.path.exists(input_file):
        print(f'Error: {input_file} does not exist.')
        return

    cookies = read_cookies(input_file)
    updated_cookies, changes = change_cookie_expiry(cookies, current_year, new_year)

    write_cookies(output_file, updated_cookies)

    print(f'Updated cookies saved to {output_file}.')
    print('\nChanges made:')
    for change in changes:
        print(change)

if __name__ == '__main__':
    main()

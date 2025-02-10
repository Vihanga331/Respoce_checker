import requests
import requests.exceptions as ex
import threading
import time

def working_domains(domain):
    result = open('result.txt', 'a')
    result.write(f'\n{domain}\n')  # Append newline for better readability
    result.close()

font = """
/$$$$$$$                                                           /$$
| $$__  $$                                                        | $$
| $$  \ $$  /$$$$$$   /$$$$$$$  /$$$$$$   /$$$$$$  /$$$$$$$   /$$$$$$$
| $$$$$$$/ /$$__  $$ /$$_____/ /$$__  $$ /$$__  $$| $$__  $$ /$$__  $$
| $$__  $$| $$$$$$$$|  $$$$$$ | $$  \ $$| $$  | $$| $$  \ $$| $$  | $$
| $$  \ $$| $$_____/ \____  $$| $$  | $$| $$  | $$| $$  | $$| $$  | $$
| $$  | $$|  $$$$$$$ /$$$$$$$/| $$$$$$$/|  $$$$$$/| $$  | $$|  $$$$$$$
|__/  |__/ \_______/|_______/ | $$____/  \______/ |__/  |__/ \_______/
                              | $$              
                              | $$                                
                              |__/        
                              
                                                          
                                                      By Dineth                           
"""

print(font)
i = 0

domain_list = open('domains.txt', 'r').read().splitlines()
print(f"{len(domain_list)} domains need to scan")
print("------------------------------------------------------------------------")


def scan_domain(domain):
    try:
        response = requests.get(f'https://{domain}', timeout=(1, 1))

        response_status = response.status_code
        response_headers = response.headers
        status_message = response.reason
        

        if response_status == 200:
            working_domains(domain)

        print(f'\n{domain} | {response_status} | {status_message}')
    except ex.RequestException as e:
        
        print(f'Error: {domain} - {e}')
    except ex.Timeout or ex.ReadTimeout:
        
        print(f'Connection Time Out: {domain}')


def main():
    start_time = time.time()

    threads = []
    max_threads = 8  # Adjust based on your CPU cores for optimal performance

    for domain in domain_list:
        if len(threads) < max_threads:
            thread = threading.Thread(target=scan_domain, args=(domain,))
            thread.start()
            threads.append(thread)
        else:
            # Wait for existing threads to finish before creating new ones
            for thread in threads:
                thread.join()
            threads.clear()

            # Create and start a new thread
            thread = threading.Thread(target=scan_domain, args=(domain,))
            thread.start()
            threads.append(thread)

    # Wait for all remaining threads to finish
    for thread in threads:
        thread.join()

    end_time = time.time()
    print(f"\nCompleted in: {end_time - start_time:.2f} seconds")


if __name__ == '__main__':
    main()

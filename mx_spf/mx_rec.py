import subprocess

def dig_mx_record(domain):
    try:
        # Run the 'dig' command to get the MX record
        result = subprocess.run(['dig', '+short', 'MX', domain], capture_output=True, text=True, check=True)
        
        # Extract hostnames from MX records
        mx_records = result.stdout.strip().split('\n')
        if mx_records and mx_records[0]:
            print(f"\nMX records for {domain}:")
            hostnames = []
            for record in mx_records:
                # Extract hostname (remove priority number)
                hostname = record.split()[-1].strip('.')
                hostnames.append(hostname)
                print(f" - {hostname}")
            return hostnames
        else:
            print(f"No MX records found for {domain}.")
            return []
    
    except subprocess.CalledProcessError as e:
        print("Error fetching MX records:", e)
        return []
    except Exception as e:
        print("An unexpected error occurred:", e)
        return []

def dig_a_record(hostname):
    try:
        # Run the 'dig' command to get the A record
        result = subprocess.run(['dig', '+short', hostname], capture_output=True, text=True, check=True)
        
        if result.stdout.strip():
            ips = result.stdout.strip().split('\n')
            print(f"A records for {hostname}:")
            for ip in ips:
                print(f" - {ip}")
            return ips
        else:
            print(f"No A records found for {hostname}.")
            return []
    
    except subprocess.CalledProcessError as e:
        print("Error fetching A records:", e)
        return []
    except Exception as e:
        print("An unexpected error occurred:", e)
        return []

if __name__ == "__main__":
    domain = input("Enter the domain: ")
    mx_hostnames = dig_mx_record(domain)
    
    if mx_hostnames:
        all_ips = []  # List to store all A record IPs
        while True:
            print("\nChoose a hostname to look up its A record (or type 'exit' to quit):")
            for i, hostname in enumerate(mx_hostnames, start=1):
                print(f"{i}. {hostname}")
            
            choice = input("Enter your choice (number or 'exit'): ").strip().lower()
            
            if choice == 'exit':
                break  # Exit the loop
            
            if choice.isdigit() and 1 <= int(choice) <= len(mx_hostnames):
                selected_hostname = mx_hostnames[int(choice) - 1]
                ips = dig_a_record(selected_hostname)
                all_ips.extend(ips)  # Store IPs in the list
                print("stored ips",all_ips)
            else:
                print("Invalid choice. Please enter a valid number or 'exit'.")
        
        # Display collected A record IPs
        print("\nCollected A record IPs:")
        for ip in set(all_ips):  # Use set to remove duplicates
            print(f" - {ip}")

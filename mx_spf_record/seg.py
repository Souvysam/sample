import requests
import dns.resolver
import ipaddress
import argparse
import constants
resolver = dns.resolver.Resolver()
resolver.timeout = 10
resolver.lifetime = 30
resolver.nameservers = ["8.8.8.8"]


def smtp_microsoft_ips(url:str)->set:
    smtp_ips=set()
    try:
        response=requests.get(url)
        if response.status_code==200:
          data=response.json()
          
        for i in data:
            if "ips" in i:
                for ip in i["ips"]:
                    smtp_ips.add(ip)
        return smtp_ips
    except Exception as e:
        print("error has been occured {}",e)
        

def mx_lookup(domain)->list:
    try:
       
        records=resolver.resolve(domain,'mx')
        mx_records=[]
        for i in records:
            data=i.exchange.to_text()
            mx_records.append(data)           
        return mx_records
    except Exception as e:
        print("{}",e)

def ips_of_domain(host_list:list)-> set:  

    iplist=set()
    try:
        for i in host_list:    
            try: 
                ips=resolver.resolve(i,'A')
                for i in ips:
                    iplist.add(i.to_text())
               
            except Exception as e:
                print("{}",e)
            
        return(iplist)
    except Exception as e :
        print("Exception as {}",e)
    
def check_seg(domain,smtp_list):
    host_list=mx_lookup(domain)
    host_ips=ips_of_domain(host_list)
    output_list=[]
    network_list=set()
    direct_ips=set()
    try:
        for i in smtp_list:
            if "/" in i:
                network_list.add(i)
            else:
                direct_ips.add(i)
        for i in host_ips:
            for j in network_list:
                network_range = ipaddress.ip_network(j, strict=False)
                if  ipaddress.ip_address(i) in network_range:
                    output_list.append(i)       
            if i in direct_ips:
                output_list.append(i)   
        if not output_list:
            print("this has  seg")
        else:
            print(output_list)
            print("this have not  seg")
    except Exception as e:
        print("exception as {}",e)
                

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--domain", type=str, required=True)
    args = parser.parse_args()
    link=constants.microsoft
    smtp_list = smtp_microsoft_ips(link)
    check_seg(args.domain, smtp_list)





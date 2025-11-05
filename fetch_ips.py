import requests
import traceback
import time
import os

# API 密钥与域名信息来自环境变量
CF_API_TOKEN = os.environ.get("CF_API_TOKEN")
CF_ZONE_ID   = os.environ.get("CF_ZONE_ID")
CF_DNS_NAME  = os.environ.get("CF_DNS_NAME")

if not all([CF_API_TOKEN, CF_ZONE_ID, CF_DNS_NAME]):
    raise SystemExit("Missing required environment variables: CF_API_TOKEN, CF_ZONE_ID, CF_DNS_NAME.")

# 仅用于获取优选 IP 的来源
def get_cf_speed_test_ip(timeout=10, max_retries=5):
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get('https://ip.164746.xyz/ipTop.html', timeout=timeout)
            if response.status_code == 200:
                return response.text
            else:
                print(f"get_cf_speed_test_ip: bad status {response.status_code} (attempt {attempt})")
        except Exception as e:
            traceback.print_exc()
            print(f"get_cf_speed_test_ip Request failed (attempt {attempt}/{max_retries}): {e}")
        time.sleep(1)
    return None

# 将优选 IP 保存到 TXT 文件
def save_ips_to_txt(ip_list, directory="ips", filename=None):
    if not ip_list:
        return None
    os.makedirs(directory, exist_ok=True)
    if filename is None:
        ts = time.strftime("%Y%m%d-%H%M%S", time.localtime())
        filename = f"preferred_ips_{ts}.txt"
    path = os.path.join(directory, filename)
    try:
        with open(path, "w", encoding="utf-8") as f:
            for ip in ip_list:
                f.write(ip.strip() + "\n")
        print(f"Saved {len(ip_list)} IPs to {path}")
        return path
    except Exception:
        traceback.print_exc()
        print("Failed to write IPs to TXT.")
        return None

def read_ips_str_to_list(ips_str):
    if not ips_str:
        return []
    return [ip.strip() for ip in ips_str.split(',') if ip.strip()]

def main():
    ip_addresses_str = get_cf_speed_test_ip()
    if not ip_addresses_str:
        print("获取 CF 优选 IP 失败，退出。")
        return

    ip_addresses = read_ips_str_to_list(ip_addresses_str)
    if not ip_addresses:
        print("解析到的 IP 为空，退出。")
        return

    save_ips_to_txt(ip_addresses)

if __name__ == '__main__':
    main()

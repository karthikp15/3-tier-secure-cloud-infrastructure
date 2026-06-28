import socket
import sys

# Define your environment variables (Replace with your actual private IPs)
APP_IP = "10.0.137.196"  # Your App Server Private IP
DB_IP = "10.0.144.55"    # Your DB Server Private IP (Update this to your actual one)

# Define the test matrix: (Test Name, Target IP, Target Port, Expected Result)
test_cases = [
    ("TC_INT_001: Web to App Management Path", APP_IP, 22, "OPEN"),
    ("TC_SEC_002: Web to App Malicious DB Path", APP_IP, 3306, "CLOSED"),
    ("TC_SEC_003: Web to DB Direct Access Path", DB_IP, 22, "CLOSED")
]

print("\n==================================================")
print("🚀 RUNNING AUTOMATED INFRASTRUCTURE VALIDATION SUITE")
print("==================================================\n")

passed_tests = 0

for name, ip, port, expected in test_cases:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3.0)
    
    result = sock.connect_ex((ip, port))
    actual = "OPEN" if result == 0 else "CLOSED"
    sock.close()
    
    if actual == expected:
        print(f"🟢 [PASS] {name}")
        print(f"         Expected: {expected} | Actual: {actual}\n")
        passed_tests += 1
    else:
        print(f"🔴 [FAIL] {name} - CRITICAL CONFIGURATION ERROR!")
        print(f"         Expected: {expected} | Actual: {actual}\n")

print("==================================================")
print(f"📊 TEST EXECUTION SUMMARY: {passed_tests}/{len(test_cases)} PASSED")
print("==================================================\n")

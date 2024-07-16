# Sachintha Fernando
# BSCP|CS|62|113

# Importing the  necessary libraries
import os
import sys
import socket
import struct
import time
import select
import random

# Define constants for ICMP packet
ICMP_REQUEST = 8
TIMEOUT = 2
PACKET_SIZE = 32
COUNT = 4

# Default timeout for waiting for ICMP responses
DEFAULT_TIMEOUT = 2


def checksum(packet):
    sum = 0

    # Ensuring count_to is even
    count_to = (len(packet) // 2) * 2

    # Initializing count to iterate through packet bytes
    count = 0

    # Process packet byte by byte
    while count < count_to:
        this_val = packet[count + 1] * 256 + packet[count]
        sum = sum + this_val
        sum = sum & 0xffffffff
        count = count + 2

    # If packet has odd number of bytes, add the last byte
    if count_to < len(packet):
        sum = sum + packet[len(packet) - 1]
        sum = sum & 0xffffffff

    # Performing the carrying propagation
    sum = (sum >> 16) + (sum & 0xffff)
    sum = sum + (sum >> 16)

    # Take one's complement to obtain final checksum
    answer = ~sum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)

    # Return the checksum value
    return answer


def receive_custom_ping(sock, timeout_duration, start_time):
    # Loop indefinitely to continuously check for incoming packets
    while True:
        ready = select.select([sock], [], [], timeout_duration)

        # If the socket is ready to read data
        if ready[0]:
            # Receive data and address from the socket
            data, addr = sock.recvfrom(1024)
            ip_header = data[:20]

            # Unpacking the IP header fields using the specified format ('!BBHHHBBH4s4s')
            ip_header_fields = struct.unpack('!BBHHHBBH4s4s', ip_header)

            ttl = ip_header_fields[5]
            icmp_header = data[20:28]

            # Unpacking the ICMP header fields using the specified format ('bbHHh')
            type, code, checksum, packet_id, sequence = struct.unpack("bbHHh", icmp_header)

            # If the ICMP packet type is 0 (ICMP Echo Reply)
            if type == 0:
                time_received = time.time()
                return time_received - start_time, addr[0], ttl

        # If the socket is not ready to read data within the timeout duration
        else:
            return None, None, None

def send_receive_ping_with_delay(sock, target_host):
    # Recording the start time when sending the ICMP echo request
    start_time = time.time()

    # Sending the ICMP echo request packet to the target host
    send_custom_ping(sock, target_host)

    # Recording the time just before receiving ICMP echo reply packets
    receive_start_time = time.time()

    # Loop indefinitely to wait for ICMP echo reply packets
    while True:
        elapsed = time.time() - receive_start_time

        # If the elapsed time exceeds the default timeout duration, return None for RTT, IP address, and TTL
        if elapsed >= DEFAULT_TIMEOUT:
            return None, None, None 

        # Attempt to receive an ICMP echo reply packet
        ping_time, ip_address, ttl = receive_custom_ping(sock, DEFAULT_TIMEOUT - elapsed, start_time)

        # If an ICMP echo reply packet is received
        if ping_time is not None:
            round_trip_time = time.time() - start_time
            return round_trip_time, ip_address, ttl

        # If no ICMP echo reply packet is received within the remaining timeout duration, return None values
        else:
            return None, None, None


def create_packet():
    # Creating the ICMP header with type 8 (ICMP Echo Request), code 0, and other fields set to 0
    header = struct.pack('bbHHh', ICMP_REQUEST, 0, 0, 0, 1)

    # Creating the data portion of the packet filled with 'x' characters
    data = b'x' * (PACKET_SIZE - struct.calcsize('bbHHh'))

    # Calculating the checksum for the combined ICMP header and data
    checksum_val = checksum(header + data)

    # Updating the ICMP header with the calculated checksum
    header = struct.pack('bbHHh', ICMP_REQUEST, 0, socket.htons(checksum_val), 0, 1)
    return header + data



def send_custom_ping(sock, target_host):
    # Creating the ICMP echo request packet using the create_packet function
    packet = create_packet()
    sock.sendto(packet, (target_host, 1))



def ping(target_host, count=COUNT):
    try:
        # Resolving the target host to its IP address
        target_ip = socket.gethostbyname(target_host)
    except socket.gaierror:
        print("Invalid destination.")
        return

    print(f"Pinging {target_host} [{target_ip}] with {PACKET_SIZE} bytes of data:")
    
    try:
        # Creating a raw socket for ICMP packets
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname("icmp"))
    except socket.error as e:
        print(f"Socket error: {e}")
        return

    # Initializing the lists to store ping times, IP addresses, and TTLs
    ping_times = []
    ip_addresses = []
    ttls = []

    # Loop for the specified number of ping attempts
    for i in range(count):
        ping_time, ip_address, ttl = send_receive_ping_with_delay(sock, target_ip)
        
        # If a reply is received
        if ping_time is not None:
            # Print information about the received reply
            print(f"Reply from {ip_address}: bytes={PACKET_SIZE}, TTL={ttl}, time={ping_time * 1000:.2f}ms")
            
            # Store ping time, IP address, and TTL
            ping_times.append(ping_time)
            ip_addresses.append(ip_address)
            ttls.append(ttl)
        else:
            print("Request timed out")

        # Sleeping for a random duration before sending the next ping
        time.sleep(random.uniform(0.5, 1.5))

    sock.close()

    # If ping responses were received
    if ping_times:
        # Print statistics about the ping process
        print(f"\nPing statistics for {target_ip}:")
        print(f"Packets: Sent = {count}, Received = {len(ping_times)}, Lost = {count - len(ping_times)}")
        print(f"Approximate round trip times in milliseconds:")
        print(f"Minimum = {min(ping_times) * 1000:.2f}ms, Maximum = {max(ping_times) * 1000:.2f}ms, Average = {sum(ping_times) / len(ping_times) * 1000:.2f}ms\n")

    # Print message indicating the end of the ping process
    print("Ping destination IP addresses in Python")


if __name__ == "__main__":
    print()
    target_host = input("Enter hostname to ping: ")
    print()
    
    # Perform the ping function with the specified hostname
    ping(target_host, COUNT)


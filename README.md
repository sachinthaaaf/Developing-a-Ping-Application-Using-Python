# Custom Ping Application

This Python program captures the characteristics of the classic Ping application, using Internet Control Message Protocol (ICMP) to enable network diagnostics smoothly and flexibly. It provides users with a powerful tool for evaluating host reachability and round-trip timings by integrating ICMP echo requests and replies into a Python framework. This application allows users to easily explore network analysis and troubleshooting complexities, highlighting the synergy between networking principles and Pythonic innovation.

## Features

- **Sending ICMP Echo Request**: Sends a single ICMP echo request to the specified target host. Builds an ICMP packet header with necessary fields and uses the socket package in Python to establish a raw socket for ICMP packet transmission.
- **Receiving ICMP Echo Reply**: Receives a single ICMP echo reply. Uses the `select` module in Python to wait for incoming packets for the specified amount of time and extracts relevant information from incoming ICMP echo reply packets.
- **Calculating Round-Trip Time**: Sends ICMP echo requests and calculates round-trip time by measuring the time interval between sending and receiving ICMP echo replies.
- **Displaying Ping Statistics**: Displays ping statistics after sending multiple ICMP echo requests. Computes packet loss, minimum, maximum, and average round-trip timings and provides useful output for each successful ping.

## Functionality

1. **Sending ICMP Echo Request**
   - `send_custom_ping(sock, target_host)`: Sends an ICMP echo request to the specified target host.

2. **Receiving ICMP Echo Reply**
   - `receive_custom_ping(sock, timeout_duration, start_time)`: Receives an ICMP echo reply and extracts information.

3. **Calculating Round-Trip Time**
   - `send_receive_ping_with_delay(sock, target_host)`: Sends ICMP echo requests and calculates round-trip time.

4. **Displaying Ping Statistics**
   - `ping(target_host, count=COUNT)`: Displays ping statistics after sending multiple ICMP echo requests.

## Usage

To use the custom Ping application, follow these steps:

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/custom-ping-application.git
   ```

2. Navigate to the project directory:
   ```sh
   cd custom-ping-application
   ```

3. Run the Ping application:
   ```sh
   python ping.py [target_host] [count]
   ```
   - `target_host`: The target host to ping (e.g., www.google.com).
   - `count`: The number of ping requests to send (default is 4).

## Summary and Reflection

This task required the creation of a custom Ping application using Python, involving networking concepts beyond the unit's scope. The learning objectives included creating, transmitting, and receiving ICMP packets, as well as displaying essential information. Through this task, I gained hands-on experience with Python programming and network diagnostics, deepening my understanding of network communication protocols and their implementation in Python. This knowledge is valuable for network administrators, developers, and IT specialists in troubleshooting network faults and optimizing connectivity.

## Created By
Sachintha Fernando

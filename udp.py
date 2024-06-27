import socket
import threading

# Fungsi untuk mengirim paket UDP ke server
def send_udp_packet(target_ip, target_port, message, count):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for _ in range(count):
        try:
            sock.sendto(message.encode(), (target_ip, target_port))
            print(f"Paket UDP dikirim ke {target_ip}:{target_port}")
        except socket.error as e:
            print(f"Gagal mengirim paket UDP: {e}")
    sock.close()

# Fungsi untuk mengirim banyak paket UDP secara paralel
def send_multiple_udp_packets(target_ip, target_port, message, count, num_threads):
    threads = []
    packets_per_thread = count // num_threads
    for _ in range(num_threads):
        thread = threading.Thread(target=send_udp_packet, args=(target_ip, target_port, message, packets_per_thread))
        thread.start()
        threads.append(thread)

    # Menunggu sampai semua thread selesai
    for thread in threads:
        thread.join()

# Main program
if __name__ == "__main__":
    target_ip = input("Masukkan IP server: ")
    target_port = int(input("Masukkan port server: "))
    message = "Test UDP packet"  # Pesan yang akan dikirim
    count = int(input("Masukkan jumlah paket yang ingin dikirim: "))
    num_threads = int(input("Masukkan jumlah thread: "))

    send_multiple_udp_packets(target_ip, target_port, message, count, num_threads)

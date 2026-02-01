"""
Memory scanner for finding War Thunder memory addresses
"""
import ctypes
from ctypes import wintypes
import struct
import time
from typing import List, Tuple, Optional

# Windows API
kernel32 = ctypes.windll.kernel32
psapi = ctypes.windll.psapi

PROCESS_VM_READ = 0x0010
PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_VM_OPERATION = 0x0008

class MemoryScanner:
    def __init__(self):
        self.process_handle = None
        self.process_id = None
        
    def enumerate_processes(self) -> List[Tuple[int, str]]:
        """List all running processes"""
        processes = []
        max_processes = 1024
        process_ids = (wintypes.DWORD * max_processes)()
        bytes_needed = wintypes.DWORD()
        
        if psapi.EnumProcesses(ctypes.byref(process_ids), 
                              ctypes.sizeof(process_ids), 
                              ctypes.byref(bytes_needed)):
            count = bytes_needed.value // ctypes.sizeof(wintypes.DWORD)
            
            for i in range(count):
                pid = process_ids[i]
                if pid == 0:
                    continue
                    
                h_process = kernel32.OpenProcess(
                    PROCESS_QUERY_INFORMATION | PROCESS_VM_READ,
                    False,
                    pid
                )
                
                if h_process:
                    try:
                        h_module = wintypes.HMODULE()
                        cb_needed = wintypes.DWORD()
                        
                        if psapi.EnumProcessModules(h_process, 
                                                   ctypes.byref(h_module),
                                                   ctypes.sizeof(h_module),
                                                   ctypes.byref(cb_needed)):
                            module_name = ctypes.create_unicode_buffer(260)
                            if psapi.GetModuleBaseNameW(h_process, 
                                                       h_module,
                                                       module_name,
                                                       ctypes.sizeof(module_name)):
                                processes.append((pid, module_name.value))
                    finally:
                        kernel32.CloseHandle(h_process)
        
        return processes
    
    def find_process(self, name: str) -> Optional[int]:
        """Find process by name"""
        name_lower = name.lower()
        processes = self.enumerate_processes()
        
        for pid, pname in processes:
            if name_lower in pname.lower():
                return pid
        return None
    
    def attach(self, pid: int) -> bool:
        """Attach to a process"""
        self.process_handle = kernel32.OpenProcess(
            PROCESS_VM_READ | PROCESS_QUERY_INFORMATION | PROCESS_VM_OPERATION,
            False,
            pid
        )
        
        if self.process_handle:
            self.process_id = pid
            return True
        return False
    
    def detach(self):
        """Detach from process"""
        if self.process_handle:
            kernel32.CloseHandle(self.process_handle)
            self.process_handle = None
            self.process_id = None
    
    def read_memory(self, address: int, size: int) -> Optional[bytes]:
        """Read memory from attached process"""
        if not self.process_handle:
            return None
        
        buffer = ctypes.create_string_buffer(size)
        bytes_read = ctypes.c_size_t()
        
        success = kernel32.ReadProcessMemory(
            self.process_handle,
            ctypes.c_void_p(address),
            buffer,
            size,
            ctypes.byref(bytes_read)
        )
        
        if success and bytes_read.value == size:
            return buffer.raw
        return None
    
    def scan_for_value(self, value: float, start_addr: int = 0x10000, 
                      end_addr: int = 0x7FFFFFFF, max_results: int = 100) -> List[int]:
        """Scan memory for a specific float value"""
        results = []
        chunk_size = 4096
        
        print(f"Scanning for value: {value}")
        print(f"Range: 0x{start_addr:X} - 0x{end_addr:X}")
        
        current_addr = start_addr
        scanned_mb = 0
        
        while current_addr < end_addr and len(results) < max_results:
            data = self.read_memory(current_addr, chunk_size)
            
            if data:
                # Search for the float value in this chunk
                for offset in range(0, len(data) - 4, 4):
                    try:
                        found_value = struct.unpack('f', data[offset:offset+4])[0]
                        if abs(found_value - value) < 0.01:  # Tolerance for floats
                            results.append(current_addr + offset)
                            if len(results) >= max_results:
                                break
                    except:
                        pass
            
            current_addr += chunk_size
            scanned_mb = (current_addr - start_addr) // (1024 * 1024)
            
            if scanned_mb % 100 == 0:
                print(f"Scanned {scanned_mb} MB... Found {len(results)} matches")
        
        return results
    
    def monitor_addresses(self, addresses: List[int], duration: int = 10):
        """Monitor addresses for changes over time"""
        print(f"\nMonitoring {len(addresses)} addresses for {duration} seconds...")
        print("(Values that change might be player coordinates, velocity, etc.)\n")
        
        initial_values = {}
        for addr in addresses:
            data = self.read_memory(addr, 4)
            if data:
                initial_values[addr] = struct.unpack('f', data)[0]
        
        time.sleep(duration)
        
        changed = []
        for addr in addresses:
            data = self.read_memory(addr, 4)
            if data:
                current_value = struct.unpack('f', data)[0]
                if addr in initial_values:
                    change = abs(current_value - initial_values[addr])
                    if change > 0.1:  # Significant change
                        changed.append((addr, initial_values[addr], current_value, change))
        
        return changed

def main():
    print("=" * 70)
    print("War Thunder Memory Scanner")
    print("=" * 70)
    print("\nThis tool helps you find memory addresses for position/entity data")
    print("WARNING: Make sure War Thunder is running BEFORE using this tool\n")
    
    scanner = MemoryScanner()
    
    # Find War Thunder process
    print("Searching for War Thunder process...")
    possible_names = ["aces.exe", "aces_BE.exe", "warthunder.exe", "WarThunder.exe"]
    
    pid = None
    for name in possible_names:
        pid = scanner.find_process(name)
        if pid:
            print(f"Found {name} (PID: {pid})")
            break
    
    if not pid:
        print("\nCouldn't find War Thunder process!")
        print("Available processes containing 'war' or 'thunder':")
        all_processes = scanner.enumerate_processes()
        for p_pid, p_name in all_processes:
            if 'war' in p_name.lower() or 'thunder' in p_name.lower() or 'ace' in p_name.lower():
                print(f"  PID {p_pid}: {p_name}")
        
        pid_input = input("\nEnter process ID manually (or press Enter to exit): ")
        if pid_input.strip():
            try:
                pid = int(pid_input)
            except:
                print("Invalid PID")
                return
        else:
            return
    
    # Attach to process
    print(f"\nAttaching to process {pid}...")
    if not scanner.attach(pid):
        print("Failed to attach to process! (Try running as Administrator)")
        return
    
    print("Successfully attached!\n")
    
    print("=" * 70)
    print("SCANNING TUTORIAL")
    print("=" * 70)
    print("""
To find player position coordinates:
1. Note your current position in War Thunder (check map coordinates)
2. Enter one coordinate value (X, Y, or Z) when prompted
3. Move your vehicle significantly 
4. Scan again with the new value to narrow down results
5. Repeat until you find the exact address

Example:
- Initial X position: 1234.5 -> Scan for 1234.5
- Move to new position: 2000.3 -> Filter results for 2000.3
- The address that matches both is your X coordinate!
""")
    
    input("Press Enter when you're ready to start scanning...")
    
    while True:
        print("\n" + "=" * 70)
        print("OPTIONS:")
        print("  1. Scan for a float value (position coordinate)")
        print("  2. Monitor addresses for changes")
        print("  3. Quick scan for coordinate ranges")
        print("  4. Exit")
        
        choice = input("\nSelect option: ").strip()
        
        if choice == "1":
            try:
                value = float(input("Enter value to search for: "))
                addresses = scanner.scan_for_value(value, max_results=1000)
                
                print(f"\nFound {len(addresses)} addresses:")
                for i, addr in enumerate(addresses[:20]):  # Show first 20
                    data = scanner.read_memory(addr, 4)
                    if data:
                        val = struct.unpack('f', data)[0]
                        print(f"  0x{addr:X}: {val:.2f}")
                
                if len(addresses) > 20:
                    print(f"  ... and {len(addresses) - 20} more")
                
                if addresses:
                    print("\nTIP: Move your vehicle and scan for the new value to narrow results")
                    save = input("Save these addresses to file? (y/n): ")
                    if save.lower() == 'y':
                        with open("wt_addresses.txt", "w") as f:
                            for addr in addresses:
                                f.write(f"0x{addr:X}\n")
                        print("Saved to wt_addresses.txt")
                
            except ValueError:
                print("Invalid value!")
        
        elif choice == "2":
            addr_file = input("Load addresses from file (wt_addresses.txt) or enter manually? (f/m): ")
            
            addresses = []
            if addr_file.lower() == 'f':
                try:
                    with open("wt_addresses.txt", "r") as f:
                        for line in f:
                            addr = int(line.strip(), 16)
                            addresses.append(addr)
                    print(f"Loaded {len(addresses)} addresses")
                except:
                    print("Couldn't load file!")
                    continue
            else:
                print("Enter addresses (hex, one per line, empty line to finish):")
                while True:
                    addr_input = input("0x")
                    if not addr_input:
                        break
                    try:
                        addresses.append(int(addr_input, 16))
                    except:
                        print("Invalid address!")
            
            if addresses:
                changed = scanner.monitor_addresses(addresses, duration=5)
                print(f"\n{len(changed)} addresses changed:")
                for addr, old_val, new_val, change in changed:
                    print(f"  0x{addr:X}: {old_val:.2f} -> {new_val:.2f} (Δ{change:.2f})")
        
        elif choice == "3":
            print("\nQuick scan for typical coordinate ranges (-5000 to 5000)")
            print("This will find all values in this range and monitor them")
            
            all_addrs = []
            for val in [-4000, -2000, 0, 2000, 4000]:
                print(f"Scanning for ~{val}...")
                addrs = scanner.scan_for_value(float(val), max_results=100)
                all_addrs.extend(addrs)
            
            print(f"\nFound {len(all_addrs)} total addresses in coordinate ranges")
            if all_addrs:
                print("Now move your vehicle and monitoring for changes...")
                changed = scanner.monitor_addresses(all_addrs[:500], duration=10)
                
                print(f"\n{len(changed)} addresses changed significantly:")
                for addr, old_val, new_val, change in sorted(changed, key=lambda x: x[3], reverse=True)[:20]:
                    print(f"  0x{addr:X}: {old_val:.2f} -> {new_val:.2f} (Δ{change:.2f})")
        
        elif choice == "4":
            break
    
    scanner.detach()
    print("\nDetached from process. Goodbye!")

if __name__ == "__main__":
    main()

"""
Memory reader for accessing War Thunder game data
"""
import ctypes
from ctypes import wintypes
import struct
from typing import Optional
from .core import Vector3


# Windows API
kernel32 = ctypes.windll.kernel32
psapi = ctypes.windll.psapi

# Process access rights
PROCESS_VM_READ = 0x0010
PROCESS_QUERY_INFORMATION = 0x0400


class MemoryReader:
    """Read-only memory access for War Thunder process"""
    
    def __init__(self, process_name: str = "aces.exe"):
        """
        Initialize memory reader
        
        Args:
            process_name: Name of the War Thunder process (default: aces.exe)
        """
        self.process_name = process_name
        self.process_handle = None
        self.base_address = None
        
    def find_process(self) -> Optional[int]:
        """
        Find War Thunder process ID
        
        Returns:
            Process ID if found, None otherwise
        """
        processes = self._enumerate_processes()
        
        for pid, pname in processes:
            if self.process_name.lower() in pname.lower():
                return pid
        
        # Try alternative names
        alt_names = ["aces_BE.exe", "warthunder.exe", "WarThunder.exe"]
        for alt_name in alt_names:
            for pid, pname in processes:
                if alt_name.lower() in pname.lower():
                    return pid
        
        return None
    
    def _enumerate_processes(self):
        """Enumerate all running processes"""
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
    
    def open_process(self, pid: int) -> bool:
        """
        Open process for reading
        
        Args:
            pid: Process ID to open
            
        Returns:
            True if successful, False otherwise
        """
        self.process_handle = kernel32.OpenProcess(
            PROCESS_VM_READ | PROCESS_QUERY_INFORMATION,
            False,
            pid
        )
        return self.process_handle is not None
    
    def close_process(self):
        """Close the process handle"""
        if self.process_handle:
            kernel32.CloseHandle(self.process_handle)
            self.process_handle = None
    
    def read_memory(self, address: int, size: int) -> Optional[bytes]:
        """
        Read memory from process
        
        Args:
            address: Memory address to read from
            size: Number of bytes to read
            
        Returns:
            Bytes read from memory, or None if failed
        """
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
    
    def read_float(self, address: int) -> Optional[float]:
        """
        Read a float from memory
        
        Args:
            address: Memory address to read from
            
        Returns:
            Float value or None if failed
        """
        data = self.read_memory(address, 4)
        if data:
            return struct.unpack('f', data)[0]
        return None
    
    def read_int(self, address: int) -> Optional[int]:
        """
        Read an integer from memory
        
        Args:
            address: Memory address to read from
            
        Returns:
            Integer value or None if failed
        """
        data = self.read_memory(address, 4)
        if data:
            return struct.unpack('i', data)[0]
        return None
    
    def read_vector3(self, address: int) -> Optional[Vector3]:
        """
        Read a 3D vector from memory
        
        Args:
            address: Memory address to read from
            
        Returns:
            Vector3 object or None if failed
        """
        data = self.read_memory(address, 12)
        if data:
            x, y, z = struct.unpack('fff', data)
            return Vector3(x, y, z)
        return None

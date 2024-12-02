import sys  # noqa: F401

# VM Constraints
MEMORY_SIZE = 0x10000 # 64KB
BIOS_MESSAGE = "Copyright (C) 2024 ZZY\n"
BOOT_MESSAGE = "Booting from hard disk...\n"
WAITING_MESSAGE = "Waiting for more instructions...\n"
ERROR_MESSAGE = "Boot signature not found. Halting.\n"

# CPU Emulatior
class CPU:
    def __init__(self, memory):
        self.memory = memory
        self.eip = 0x7C00  # Start exec at the bootloader
        self.running = True

    def fetch(self): # Fetch the next instruction (1 byte at a time)
        return self.memory[self.eip]
    
    def execute(self, opcode): # Execute the instruction
        if opcode == 0xEB:  # JMP (near jump)
            offset = self.memory[self.eip + 1] # This is `jmp $` (infinite loop)
            if offset == 0xFE:
                self.running = False  # Stop execution
            else:
                self.eip += 2 + offset  # Move instruction pointer
        elif opcode == 0x00:  # Padding (NOP-like behavior for filler bytes)
            self.eip += 1
        else:
            print(f"Unsupported opcode {opcode:02X} at {self.eip:04X}. Halting.")
            self.running = False

# Virtual Machine
class VM:
    def __init__(self):
        self.memory = bytearray(MEMORY_SIZE)
        self.cpu = CPU(self.memory)

    def load_bin(self, filename:str): # Load the binary into the memory at 0x7C00
        with open(filename, "rb") as f:
            bootloader = f.read()
            if len(bootloader) > 512:
                raise ValueError("Bootloader too large!")
            
            self.memory[0x7C00:0x7C00 + len(bootloader)] = bootloader

    def display_message(self, message:str): # Show the BIOS-style interface
        print(message, end="")

    def run(self): # Run the VM
        # Show the BIOS-style interface
        self.display_message(BIOS_MESSAGE) # 第一句

        # Check if bootloader contains the boot signature
        if self.memory[0x7DFE] == 0x55 and self.memory[0x7DFF] == 0xAA:
            self.display_message(BOOT_MESSAGE) # 第二句
        else:
            self.display_message(ERROR_MESSAGE)
            return

        # Execute the bootloader
        while self.cpu.running:
            opcode = self.cpu.fetch()
            self.cpu.execute(opcode)

        # After execution stops
        self.display_message(WAITING_MESSAGE) # 第三句

# Main Entry Point
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python VMRunner.py <bootloader.bin>. (Now this means: python VMRunner.py path\\to\\your\\bootloader.bin)")
        sys.exit(1)

#THANK·YOU!
# Code Autocomplete is made by MarsCode AI, Doubao. Extension available thru VSCode Marketplace.
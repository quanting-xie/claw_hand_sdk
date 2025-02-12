import can
import struct
import odrive

class Motor:
    def __init__(self, bus, node_id):
        """Initialize a Driver instance for an ODrive board."""
        self.bus = bus
        self.node_id = node_id
    
    def send_command(self, command_id, data):
        """Send a CAN message with the given command and data."""
        arbitration_id = (self.node_id << 5) | command_id
        message = can.Message(arbitration_id=arbitration_id, data=data, is_extended_id=False)
        self.bus.send(message)
    
    def set_velocity(self, velocity):
        """Set motor velocity."""
        data = struct.pack('<f', velocity)  # Convert float to 4-byte data
        self.send_command(0x07, data)  # Assuming 0x07 is the velocity control command
    
    def get_feedback(self):
        """Request and receive motor feedback."""
        self.send_command(0x09, [])  # Request feedback (example command ID)
        msg = self.bus.recv(1.0)  # Wait for response
        if msg and msg.arbitration_id == ((self.node_id << 5) | 0x09):
            pos, vel, curr = struct.unpack('<fff', msg.data)
            return {'position': pos, 'velocity': vel, 'current': curr}
        return None
    
    def close(self):
        """Close the CAN bus."""
        self.bus.shutdown()

# Example usage
if __name__ == "__main__":
    odrive = Motor(can.interface.Bus(bustype='socketcan', channel='vcan0'), node_id=0x01)
    odrive.set_velocity(1000.0)
    position, velocity = odrive.get_feedback()
    print(f"Position: {position}, Velocity: {velocity}")
    odrive.close()

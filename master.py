import can
import struct
import time
from driver import Motor

class Master:
    def __init__(self, channel='can0', bustype='socketcan'):
        """Initialize the master to manage multiple drivers over CAN."""
        self.bus = can.interface.Bus(channel=channel, bustype=bustype)
        self.motors = {}
    
    def add_driver(self, node_id):
        """Register a new driver."""
        self.motors[node_id] = Motor(self.bus, node_id)
    
    def set_all_velocities(self, velocity):
        """Set the same velocity for all drivers."""
        for motor in self.motors.values():
            motor.set_velocity(velocity)
    
    def get_all_feedback(self):
        """Retrieve feedback from all drivers."""
        feedback = {}
        for node_id, motor in self.motors.items():
            feedback[node_id] = motor.get_feedback()
        return feedback
    def set_all_positions(self, position):
        """Set the same position for all drivers."""
        for motor in self.motors.values():
            motor.set_position(position)
    
    def set_velocity(self, node_id, velocity):
        """Set the velocity for a specific driver."""
        self.motors[node_id].set_velocity(velocity)
    
    def close(self):
        """Close the CAN bus connection."""
        self.bus.shutdown()

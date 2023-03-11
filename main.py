import tkinter as tk
import numpy as np
import can
import struct
import serial
import serial.tools.list_ports

CAN_MESSAGE_ID_SEND = 0x0D1

class OUR_Monitor:
    def __init__(self, voltages, temperatures):

        # Create the GUI window
        self.window = tk.Tk()
        self.window.title("OUR Battery Monitor")

        # Create the two listbox widgets and populate them with the initial values
        self.V_frame = tk.Frame(self.window)
        self.listboxV=[]
        for i in range(9):
            self.listboxV.append(tk.Listbox(self.V_frame))
            for j in range(3):
                index = i*3 + j
                self.listboxV[i].insert(tk.END, f"Voltage {index}: {voltages[index]}")

        self.T_frame = tk.Frame(self.window)
        self.listboxT=[]
        for i in range(9):
            self.listboxT.append(tk.Listbox(self.T_frame))
            for j in range(6):
                index = i*6 + j
                if index < len(temperatures):
                    self.listboxT[i].insert(tk.END, f"Temperature {index}: {temperatures[index]}")

        # Add the two listboxes to the frame
        start_row=2
        n_col=3
        n_row=3
        for i in range(9):
            self.listboxV[i].grid(row=i // n_row+ start_row, column=i % n_col , padx=5, pady=5)
        for i in range(9):
            self.listboxT[i].grid(row=i // n_row + start_row, column=i % n_col + n_col, padx=5, pady=5)


        # Create a frame to group the input box and button and connect button
        self.input_frame = tk.Frame(self.window)

        # Add a label and text entry widget to the input frame
        self.input_label = tk.Label(self.input_frame, text="Discharge current limit:")
        self.input_entry = tk.Entry(self.input_frame)

        # Add the label and text entry widget to the input frame
        self.input_label.pack(side=tk.LEFT)
        self.input_entry.pack(side=tk.LEFT)

        # Add a button to send the value via a CAN message
        self.send_button = tk.Button(self.input_frame, text="Send", command=self.send_DCL)
        self.send_button.pack(side=tk.LEFT)

        # Create a button to connect to the CANadapter
        connect_button = tk.Button(self.input_frame, text="Connect to CANadapter", command=self.connect_to_CANadapter)
        connect_button.pack(side=tk.RIGHT)

        # Add frame with the parameter read out
        self.value_readout = tk.Frame(self.window)
        # Create a frame to hold the value readout
        value_readout_frame = tk.Frame(self.window, bd=2, relief=tk.SUNKEN)


        # Define the sensor values and their units
        sensor_values = [
            ("Temperature", "°C"),
            ("Humidity", "%"),
            ("Pressure", "kPa"),
            ("Voltage", "V"),
            ("Current", "A"),
            ("Power", "W"),
            ("Speed", "km/h"),
            ("Altitude", "m"),
            ("Acceleration", "m/s^2"),
            ("Gyro", "°/s"),
            ("Magnetometer", "μT"),
            ("GPS", ""),
        ]

        # Create the labels and values for each sensor value
        for i, (label, unit) in enumerate(sensor_values):
            # Calculate the row and column for the label and value
            row = i // 6
            col = i % 6

            # Create the label for the sensor value
            label_text = f"{label}:"
            label_widget = tk.Label(value_readout_frame, text=label_text)
            label_widget.grid(row=row, column=2 * col, padx=5, pady=5)

            # Create the value for the sensor value
            value_widget = tk.Label(value_readout_frame, text="--.--", font=("Arial", 16), width=6)
            value_widget.grid(row=row, column=2 * col + 1, padx=5, pady=5)

            # Create the unit for the sensor value
            unit_widget = tk.Label(value_readout_frame, text=unit)
            unit_widget.grid(row=row, column=2 * col + 2, padx=5, pady=5)
        # Add the input frame to the window
        self.input_frame.pack(side=tk.TOP)
        value_readout_frame.pack(padx=10, pady=10, side=tk.TOP)
        self.V_frame.pack(side=tk.LEFT)
        self.T_frame.pack(side=tk.RIGHT)

        self.window.mainloop()

    def connect_to_CANadapter(self):
        # Create a new window to select the COM port
        connect_window = tk.Toplevel(self.window)
        connect_window.title("Select COM port")

        # create two frames for dropdowns and menus
        port_frame = tk.Frame(connect_window)
        baudrate_frame = tk.Frame(connect_window)
        # Add labels to dropdowns
        port_label = tk.Label(port_frame, text="Port:")
        port_label.pack(side=tk.LEFT)

        port_label = tk.Label(baudrate_frame, text="Baudrate:")
        port_label.pack(side=tk.LEFT)

        port_label = tk.Label(baudrate_frame, text="kbit")
        port_label.pack(side=tk.RIGHT)
        # Get a list of all available COM ports
        ports = [p.device for p in serial.tools.list_ports.comports()]
        baudrates = [250, 500, 1000]
        # Create a dropdown menu to select the COM port
        selected_port = tk.StringVar()
        CAN_baudrate = tk.StringVar()
        # initial menu text
        selected_port.set(ports[0])
        CAN_baudrate.set(250)
        port_menu = tk.OptionMenu(port_frame, selected_port, *ports)
        can_baudrate_menu = tk.OptionMenu(baudrate_frame, CAN_baudrate, *baudrates)
        port_menu.pack(side=tk.LEFT)
        can_baudrate_menu.pack(side=tk.LEFT)

        port_frame.pack()
        baudrate_frame.pack()

        # Create a button to connect to the selected COM port
        def connect_to_port(self):
            # Initialise CAN
            try:
                self.CANbus = can.interface.Bus(bustype='serial', channel=str(selected_port.get()), bitrate=int(CAN_baudrate.get())*1000)
                print("Connected to "+selected_port.get())
            except Exception as e:
                print("Could not connect to serial CAN interface")
                print(e)
            connect_window.destroy()

        connect_button = tk.Button(connect_window, text="Connect", command= lambda: connect_to_port(self))
        connect_button.pack()

    def send_DCL(self):
        # Get the value from the text entry widget
        if self.CANbus:
            value = self.input_entry.get()

            # Send the value via a CAN message (replace with actual code)
            print(f"Sending value: {value}")
            struct.pack()
            msg = can.Message(arbitration_id=CAN_MESSAGE_ID_SEND,data=[],dlc=2)
            self.CANbus.send()

    def update(self, list1, list2):
        # Clear the existing values in the listbox widgets
        for i in range(9):
            for j in range(3):
                index = i*3 + j
                self.listboxV[i].delete(0, tk.END)

        for i in range(9):
            for j in range(6):
                index = i*6 + j
                if index < len(list2):
                    self.listboxT[i].delete(0, tk.END)
        # Add the new values to the listbox widgets
        for i in range(9):
            for j in range(3):
                index = i*3 + j
                if index < len(list1):
                    self.listbox.insert(tk.END, f"Voltage {index}: {list1[index]}")

        for i in range(9):
            for j in range(6):
                index = i*6 + j
                if index < len(list2):
                    self.listbox2.insert(tk.END, f"Value {index}: {list2[index]}")

if __name__ == "__main__":
    # Example usage
    V = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]
    T = [1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9, 10.1, 11.2, 12.3, 13.4, 14.5, 15.6, 16.7, 17.8, 18.9, 19.1, 20.2, 21.3, 22.4, 23.5, 24.6, 25.7, 26.8, 27.9, 28.1, 29.2, 30.3, 31.4, 32.5, 33.6, 34.7, 35.8, 36.9, 37.1, 38.2, 39.3]

    gui = OUR_Monitor(V, T)
    gui.update(V, T)

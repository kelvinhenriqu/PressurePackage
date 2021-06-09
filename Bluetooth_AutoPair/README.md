# PressurePackage


> This routine allows any device to pair to raspberry without any action of pi's side

To do this you need to :

1. Create a file called "/usr/local/bin/auto-agent" containing the following code.

```python
#!/usr/bin/python

from __future__ import absolute_import, print_function, unicode_literals

from optparse import OptionParser
import sys
import dbus
import dbus.service
import dbus.mainloop.glib
try:
  from gi.repository import GObject
except ImportError:
  import gobject as GObject
import bluezutils

BUS_NAME = 'org.bluez'
AGENT_INTERFACE = 'org.bluez.Agent1'
AGENT_PATH = "/test/agent"

bus = None
device_obj = None
dev_path = None

def ask(prompt):
	try:
		return raw_input(prompt)
	except:
		return input(prompt)

def set_trusted(path):
	props = dbus.Interface(bus.get_object("org.bluez", path),
					"org.freedesktop.DBus.Properties")
	props.Set("org.bluez.Device1", "Trusted", True)

def dev_connect(path):
	dev = dbus.Interface(bus.get_object("org.bluez", path),
							"org.bluez.Device1")
	dev.Connect()

class Rejected(dbus.DBusException):
	_dbus_error_name = "org.bluez.Error.Rejected"

class Agent(dbus.service.Object):
	exit_on_release = True

	def set_exit_on_release(self, exit_on_release):
		self.exit_on_release = exit_on_release

	@dbus.service.method(AGENT_INTERFACE,
					in_signature="", out_signature="")
	def Release(self):
		print("Release")
		if self.exit_on_release:
			mainloop.quit()

	@dbus.service.method(AGENT_INTERFACE,
					in_signature="os", out_signature="")
	def AuthorizeService(self, device, uuid):
		print("AuthorizeService (%s, %s)" % (device, uuid))
		return # automatically authorize connection
		authorize = ask("Authorize connection (yes/no): ")
		if (authorize == "yes"):
			return
		raise Rejected("Connection rejected by user")

	@dbus.service.method(AGENT_INTERFACE,
					in_signature="o", out_signature="s")
	def RequestPinCode(self, device):
		print("RequestPinCode (%s)" % (device))
		set_trusted(device)
		#return ask("Enter PIN Code: ")
		return "0000" # return default PIN Code of 0000

	@dbus.service.method(AGENT_INTERFACE,
					in_signature="o", out_signature="u")
	def RequestPasskey(self, device):
		print("RequestPasskey (%s)" % (device))
		set_trusted(device)
		#passkey = ask("Enter passkey: ")
		passkey = "0000" # return default passkey of 0000
		return dbus.UInt32(passkey)

	@dbus.service.method(AGENT_INTERFACE,
					in_signature="ouq", out_signature="")
	def DisplayPasskey(self, device, passkey, entered):
		print("DisplayPasskey (%s, %06u entered %u)" %
						(device, passkey, entered))

	@dbus.service.method(AGENT_INTERFACE,
					in_signature="os", out_signature="")
	def DisplayPinCode(self, device, pincode):
		print("DisplayPinCode (%s, %s)" % (device, pincode))

	@dbus.service.method(AGENT_INTERFACE,
					in_signature="ou", out_signature="")
	def RequestConfirmation(self, device, passkey):
		print("RequestConfirmation (%s, %06d)" % (device, passkey))
		set_trusted(device)
		return # automatically trust
		confirm = ask("Confirm passkey (yes/no): ")
		if (confirm == "yes"):
			set_trusted(device)
			return
		raise Rejected("Passkey doesn't match")

	@dbus.service.method(AGENT_INTERFACE,
					in_signature="o", out_signature="")
	def RequestAuthorization(self, device):
		print("RequestAuthorization (%s)" % (device))
		return # automatically authorize
		auth = ask("Authorize? (yes/no): ")
		if (auth == "yes"):
			return
		raise Rejected("Pairing rejected")

	@dbus.service.method(AGENT_INTERFACE,
					in_signature="", out_signature="")
	def Cancel(self):
		print("Cancel")

def pair_reply():
	print("Device paired")
	set_trusted(dev_path)
	dev_connect(dev_path)
	mainloop.quit()

def pair_error(error):
	err_name = error.get_dbus_name()
	if err_name == "org.freedesktop.DBus.Error.NoReply" and device_obj:
		print("Timed out. Cancelling pairing")
		device_obj.CancelPairing()
	else:
		print("Creating device failed: %s" % (error))


	mainloop.quit()

if __name__ == '__main__':
	dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

	bus = dbus.SystemBus()

	capability = "KeyboardDisplay"

	parser = OptionParser()
	parser.add_option("-i", "--adapter", action="store",
					type="string",
					dest="adapter_pattern",
					default=None)
	parser.add_option("-c", "--capability", action="store",
					type="string", dest="capability")
	parser.add_option("-t", "--timeout", action="store",
					type="int", dest="timeout",
					default=60000)
	(options, args) = parser.parse_args()
	if options.capability:
		capability  = options.capability

	path = "/test/agent"
	agent = Agent(bus, path)

	mainloop = GObject.MainLoop()

	obj = bus.get_object(BUS_NAME, "/org/bluez");
	manager = dbus.Interface(obj, "org.bluez.AgentManager1")
	manager.RegisterAgent(path, capability)

	print("Agent registered")

	# Fix-up old style invocation (BlueZ 4)
	if len(args) > 0 and args[0].startswith("hci"):
		options.adapter_pattern = args[0]
		del args[:1]

	if len(args) > 0:
		device = bluezutils.find_device(args[0],
						options.adapter_pattern)
		dev_path = device.object_path
		agent.set_exit_on_release(False)
		device.Pair(reply_handler=pair_reply, error_handler=pair_error,
								timeout=60000)
		device_obj = device
	else:
		manager.RequestDefaultAgent(path)

	mainloop.run()

	#adapter.UnregisterAgent(path)
	#print("Agent unregistered")
```

2. Make file executable
```python
sudo chmod +x /usr/local/bin/auto-agent
```

3. Create a file called "/usr/local/bin/bluezutils.py" containing the following code.
```python
import dbus

SERVICE_NAME = "org.bluez"
ADAPTER_INTERFACE = SERVICE_NAME + ".Adapter1"
DEVICE_INTERFACE = SERVICE_NAME + ".Device1"

def get_managed_objects():
	bus = dbus.SystemBus()
	manager = dbus.Interface(bus.get_object("org.bluez", "/"),
				"org.freedesktop.DBus.ObjectManager")
	return manager.GetManagedObjects()

def find_adapter(pattern=None):
	return find_adapter_in_objects(get_managed_objects(), pattern)

def find_adapter_in_objects(objects, pattern=None):
	bus = dbus.SystemBus()
	for path, ifaces in objects.iteritems():
		adapter = ifaces.get(ADAPTER_INTERFACE)
		if adapter is None:
			continue
		if not pattern or pattern == adapter["Address"] or \
							path.endswith(pattern):
			obj = bus.get_object(SERVICE_NAME, path)
			return dbus.Interface(obj, ADAPTER_INTERFACE)
	raise Exception("Bluetooth adapter not found")

def find_device(device_address, adapter_pattern=None):
	return find_device_in_objects(get_managed_objects(), device_address,
								adapter_pattern)

def find_device_in_objects(objects, device_address, adapter_pattern=None):
	bus = dbus.SystemBus()
	path_prefix = ""
	if adapter_pattern:
		adapter = find_adapter_in_objects(objects, adapter_pattern)
		path_prefix = adapter.object_path
	for path, ifaces in objects.iteritems():
		device = ifaces.get(DEVICE_INTERFACE)
		if device is None:
			continue
		if (device["Address"] == device_address and
						path.startswith(path_prefix)):
			obj = bus.get_object(SERVICE_NAME, path)
			return dbus.Interface(obj, DEVICE_INTERFACE)

	raise Exception("Bluetooth device not found")
```

4. Create a file called "BtAutoPair.py" (you can save this anywhere convenient) containing the following code.
```python
#!/usr/bin/python
# encoding=utf8

import sys
import time
import pexpect
import subprocess

class BtAutoPair:
	"""Class to auto pair and trust with bluetooth."""

	def __init__(self):
		p = subprocess.Popen("/usr/local/bin/auto-agent", shell = False)
		out = subprocess.check_output("/usr/sbin/rfkill unblock bluetooth", shell = True)
		self.child = pexpect.spawn("bluetoothctl", echo = False)

	def get_output(self,command, pause = 0):
		"""Run a command in bluetoothctl prompt, return output as a list of lines."""
		self.child.send(command + "\n")
		time.sleep(pause)
		start_failed = self.child.expect(["bluetooth", pexpect.EOF])

		if start_failed:
			raise BluetoothctlError("Bluetoothctl failed after running " + command)
			
		return self.child.before.split("\r\n")

	def enable_pairing(self):
		"""Make device visible to scanning and enable pairing."""
		print "pairing enabled"
		try:
			out = self.get_output("power on")
			out = self.get_output("discoverable on")
			out = self.get_output("pairable on")
			out = self.get_output("agent off")

		except BluetoothctlError, e:
			print(e)
			return None

	def disable_pairing(self):
		"""Disable devices visibility and ability to pair."""
		try:
			out = self.get_output("discoverable off")
			out = self.get_output("pairable off")

		except BluetoothctlError, e:
			print(e)
			return None
```

5. Create a file called "AutoPair.py (save this in the same directory as BtAutoPair.py) containing the following code.
```python
#!/usr/bin/python

import BtAutoPair

autopair = BtAutoPair.BtAutoPair()

autopair.enable_pairing()
```

6. You will need to install these repositories if it's not already installed.
```terminal
sudo apt install python-pexpect
sudo apt install python-dbus
```

7. To make the Pi permanently discoverable edit "/etc/bluetooth/main.conf" and change the line removing # :
```terminal
#DiscoverableTimeout = 0
```

## 📫 Connections :

[![Main](https://img.shields.io/badge/Main%20-%23323330.svg?&style=for-the-badge&logo=Main%20ff&logoColor=black&color=8000FF)](https://github.com/kelvinhenriqu/PressurePackage/tree/main)
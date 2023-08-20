import frida
import time
import os
import re

class Decryptor():

    script_name = "_agent.js"
    script_inject = "_inject.js"
    DecryptorNativeFnc = None

    def __init__(self, file, pid, gadget, lua_header):
        self.lua_header = lua_header
        try:
            self.device = frida.get_usb_device()
            if file:
                pid = self.device.spawn([file])
                device.resume(pid)
                time.sleep(1)
                self.session = self.device.attach(pid)
            elif pid:
                self.session = self.device.attach(int(pid))
            elif gadget:
                self.gadget_run(gadget)
            else:
                exit("[-] Error: No file or pid provided")
        except frida.ProcessNotFoundError as e:
            exit("[-] Error: Process not found")
        except Exception as e:
            exit("[-] Error: " + str(e))
    
    def gadget_run(self, package_activity):
        package,activity = package_activity.split("/")
        # Run ADB
        os.system("adb shell am force-stop " + package)
        os.system("adb shell am start -n " + package_activity)
        pid = os.popen('adb shell "ps -A | grep '+package+'"').read()
        time.sleep(2)
        pid = re.findall(r"\b\d+\b", pid)[0]
        self.session = self.device.attach(int(pid))
        print(self.session)

    def on_error(self, session, error):
        print("[-] Error: " + error)
        exit()

    def on_message(self, message, data):
        if message["type"] == "send":
            if message["payload"].startswith("[+] XXTEA:"):
                # Parse Arguments
                groups = re.search(r"A1:(?P<A1>[^ ]+) A2:(?P<A2>[^ ]+) A3:(?P<A3>[^ ]+) A4:(?P<A4>[^ ]+)",message["payload"])
                if groups:
                    with open(self.script_inject) as f:
                        script_code = f.read()
                        script_code = script_code.replace("AGENT_LIB_NAME", self.lib)
                        script_code = script_code.replace("XXTEA_DECRYPT_OFFSET", self.offset)
                        script_code = script_code.replace("KEY_ARRAY", groups.group("A2"))
                        script_code = script_code.replace("KEY_LENGTH", groups.group("A3"))
                        script_code = script_code.replace("ARRAY_5", groups.group("A4"))
                        self.decryptor_script = self.session.create_script(script_code)
                        # print(script_code)
                    self.decryptor_script.on("message", self.on_message)
                    self.decryptor_script.load()
                    self.DecryptorNativeFnc = self.decryptor_script.exports.XXTEADECRYPT

    def get_file_byte_array(self, file):
        with open(file, "rb") as f:
            byte_array = f.read()
            if not byte_array.startswith(self.lua_header.encode()):
                exit("[-] Error: Invalid lua header(" + self.lua_header + ")")
            byte_array =  byte_array[len(self.lua_header):]
            fileSz = len(byte_array)
            int_array = [b for b in byte_array]
            return int_array, fileSz

    def folder_decrypt(self, folder):
        # Walk through folder
        for root, dirs, files in os.walk(folder):
            for file in files:
                if file.endswith(".luac"):
                    file_path = os.path.join(root, file)
                    print("[+] Decrypting file: " + file_path)
                    arr,sz = self.get_file_byte_array(file_path)
                    response = self.DecryptorNativeFnc(arr, sz)
                    if response:
                        with open(file_path.replace("luac","lua"), "wb") as f:
                            f.write(response.encode())
                    else:
                        exit("[-] Error: Decryption failed")

    def run(self, folder, lib, offset):
        try:
            self.lib = lib
            self.offset = offset
            time.sleep(2)
            if self.session:
                with open(self.script_name) as f:
                    script_code = f.read()
                    script_code = script_code.replace("AGENT_LIB_NAME", lib)
                    script_code = script_code.replace("XXTEA_DECRYPT_OFFSET", offset)

                    script = self.session.create_script(script_code)
                script.on("message", self.on_message)
                script.load()
                print("[+] Script loaded")
                while self.DecryptorNativeFnc == None:
                    print("[+] Waiting for XXTEA decrypt function...")
                    time.sleep(2)
                print("[+] XXTEA decrypt function found")
                self.folder_decrypt(folder)
            else:
                exit("[-] Error: No session")
        except Exception as e:
            exit("[-] Error: " + str(e))
            self.device.close()
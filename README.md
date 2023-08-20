# COCOS2dx LUAC Runtime Decryptor
A tool built on python & frida to automatically decrypt the `.luac` files of COCOS2dx games. Please remember that this has only been tested on Mobile games.
## Installation
```python -m pip install -r requirements.txt```
## Finding Required Information
Before you start using this tool you will need gather the following 3 information manually.
1. Library Name that contains the decryptor (Default: `libqpry_lua.so`). You can find this library in the `libs/{ARCH}/` folder of the extracted application.
2. Next you will have to decompile this native library in `Ghidra` or `IDA-PRO` to find the offset of the `xxtea_decrypt` function. In Ghidra, the offset will be `ADDRESS-10000`. Refer to screenshots for reference.

![Ghidra Function Search](https://i.imgur.com/00KY5ak.png)
![XXTEA_DECRYPT OFFSET](https://i.imgur.com/95lP8zW.png)

3. Finally, we will be needing the fetching the header from the `.luac` file.
![LUAC HEADER](https://i.imgur.com/Ef23kLA.png)


## Usage
Finally we will use this information to decrypt all the files.
### FLAG: `-f|--file`
This will allow you to spawn the application on the mobile device and hook frida to it automatically. Frida server will be required
```python main.py -f PACKAGE_NAME```

### FLAG: `-p|--pid`
If you are using frida gadget with an application and you want to the decryptor to hook to the pid, then you can use this flag.
```python main.py -p GADGET_PID```

### FLAG: `-g|--gadget`
Similar to `-p|--pid`, except that the tool automatically spawn and hooks to the application, eliminating the need to manually fetch the gadget PID. This method only works for android devices.
```python main.py -g PACKAGE_NAME/MAIN_LAUNCHER_ACTIVITY```

### Usage Examples
Following are some of the examples on how you can use the tool.
```
python main.py -f com.example.cocos2dx -l libtest.so -o 0x002Da542 --lua-header "TEST_LUA_HDR" --folder ./apktool_out/assets/base/
python main.py -p 5341 -l libtest.so -o 0x002Da542 --lua-header "TEST_LUA_HDR" --folder ./apktool_out/assets/base/
python main.py -g com.example.cocos2dx/com.example.cocos2dx.Appactivity -l libtest.so -o 0x002Da542 --lua-header "TEST_LUA_HDR" --folder ./apktool_out/assets/base/
```

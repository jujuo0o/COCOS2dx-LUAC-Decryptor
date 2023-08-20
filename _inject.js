
var il2cpp_module_addr = Module.findBaseAddress("AGENT_LIB_NAME");

// Create Native Function for XXTEA Decrypt
var xxtea_decrypt = new NativeFunction(
    il2cpp_module_addr.add("XXTEA_DECRYPT_OFFSET"),
    'pointer', ['pointer', 'int', 'pointer', 'int', 'pointer']
);
function XXTEADECRYPT(a1, a2){
    if(il2cpp_module_addr!=null){
        //  Allocate Memory For the LUAC File
        var m_alloc_addr = Memory.alloc(a2);
        // Write the LUAC File to the Memory
        m_alloc_addr.writeByteArray(a1);
    
        // Call XXTEA Decrypt and get the return value
        var str_ptr = xxtea_decrypt(
            m_alloc_addr,
            a2,
            ptr(KEY_ARRAY),
            KEY_LENGTH,
            ptr(ARRAY_5)
        );
    
        return str_ptr.readCString();
        
    }
    return "";
}


rpc.exports = {
    xxteadecrypt: XXTEADECRYPT
};
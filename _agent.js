var il2cpp_module_addr = Module.findBaseAddress("AGENT_LIB_NAME");
if(il2cpp_module_addr!=null){
    Interceptor.attach(il2cpp_module_addr.add("XXTEA_DECRYPT_OFFSET"), 
    {
        onEnter: function(args) {
            send("[+] XXTEA: A1:"+args[1].toString()+" A2:"+args[2].toString()+" A3:"+args[3].toString()+" A4:"+args[4].toString())
        },
        onLeave: function(retval) {
        }
    });

}
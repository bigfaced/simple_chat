async function keepalive(){
    let f=await fetch("/api/keepalive");
    console.log(Date.now(), "Keep alive", f);
    setTimeout(keepalive, 10000)
}

keepalive();
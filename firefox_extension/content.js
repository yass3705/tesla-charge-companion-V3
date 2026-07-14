
window.addEventListener('message',event=>{
 if(event.source!==window||event.origin!==window.location.origin)return;
 const m=event.data||{};if(m.source!=='tcc-app')return;
 if(m.type==='TCC_PING')window.postMessage({source:'tcc-extension',type:'TCC_PONG'},window.location.origin);
 if(m.type==='TCC_START')browser.runtime.sendMessage({type:'start-update',stations:m.stations});
 if(m.type==='TCC_STOP')browser.runtime.sendMessage({type:'stop-update'});
});
browser.runtime.onMessage.addListener(m=>{
 if(m.type==='progress')window.postMessage({source:'tcc-extension',type:'TCC_PROGRESS',current:m.current,total:m.total,text:m.text},window.location.origin);
 if(m.type==='finished')window.postMessage({source:'tcc-extension',type:'TCC_FINISHED',success:m.success,text:m.text},window.location.origin);
});
window.postMessage({source:'tcc-extension',type:'TCC_PONG'},window.location.origin);

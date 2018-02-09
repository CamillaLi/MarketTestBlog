function ResizeImage(objImage,maxWidth){ 
try{ 
 if(maxWidth>0){ 
  if(objImage.width>maxWidth){ 
   objImage.width=maxWidth; 
    if (window.attachEvent) 
     {objImage.attachEvent('onclick', function(){try{window.open(objImage.src);}catch(e){window.open(objImage.src);}}); 
      objImage.attachEvent('onmouseover', function(){objImage.style.cursor='pointer';}); 
     } 
     if (window.addEventListener) 
     {objImage.addEventListener('click', function(){try{window.open(objImage.src);}catch(e){window.open(objImage.src);}},false); 
     objImage.addEventListener('mouseover', function(){objImage.style.cursor='pointer';},false); 
     }     
  } 
 } 
}catch(e){}; 
}
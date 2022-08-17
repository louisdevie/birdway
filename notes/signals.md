```
SIGNAL
├─ SUCCESS
├─ ERR_ANY
│  ├─ ERR_VALUE
│  │  ├─ ERR_NULL
│  │  ├─ ERR_MATH
│  │  └─ ERR_OVERFLOW
│  ├─ ERR_OS
│  │  ├─ ERR_IO
│  │  ├─ ERR_NOTFOUND
│  │  ├─ ERR_PERM
│  │  ├─ ERR_NOTAFILE
│  │  ├─ ERR_NOTADIR
│  │  └─ ERR_EXISTS
│  ├─ ERR_LOOKUP
│  ├─ ERR_FORMAT
│  ├─ ERR_USERINT
│  ├─ ERR_MEMORY
│  └─ FAIL
├─ RETURN
├─ BREAK
└─ SKIP
```

The signals `SIGNAL`, `BREAK`, `SKIP` and `RETURN` doesn't have a predefined constant.
`SIGNAL` should never be thrown, and the three others are thrown using specific statements
(`break`, `skip` and `return`).

Any other signal can be thrown with a `throw` and caught with a `try`.

Name        |Meaning                         
------------|---------------------------------
BREAK       |Loop break                       
ERR_ANY     |Base error                       
ERR_EXISTS  |File/directory already exists    
ERR_IO      |I/O error                        
ERR_LOOKUP  |Invalid index or key             
ERR_MATH    |Invalid math operation           
ERR_MEMORY  |Memory error                     
ERR_NOTADIR |A directory was expected         
ERR_NOTAFILE|A file was expected              
ERR_NOTFOUND|A path doesn't exists            
ERR_NULL    |A nullable value was NULL        
ERR_OS      |Base OS error                    
ERR_APP     |Error specific to the application
ERR_OVERFLOW|Integer overflow/underflow       
ERR_PERM    |Permission denied                
ERR_USERINT |User interrupt (e.g. Ctrl+C)     
ERR_VALUE   |Base value error   
FAIL        |Generic error
ERR_FORMAT  |Invalid input format              
RETURN      |Function return                  
SIGNAL      |Abstract base signal             
SKIP        |Loop skip                        
SUCCESS     |Exit the program successfully    


The `error` statement allocates new error signals:
* `error ERR_A` creates a new signal children of `ERR_APP`,
  with an associated exit code. There are a maximum of 30 that
  may be allocated.
* `error ERR_B is ERR_A` creates a new signal children of `ERR_A`
  that inherits the return code from its parent.

Only one base error should be created by application / library.
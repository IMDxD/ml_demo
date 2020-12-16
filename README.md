# ML demo style GAN

Styles are located at
https://drive.google.com/drive/folders/17vHbpOCWLDL65F6Yk-jEwQlpQ4pHYjqD?usp=sharing
and must be placed at the "styles" folder


Code to test app

```
with open("test_imgs/test.png", "rb") as file:
    r = requests.post("http://127.0.0.1:5000/sunset", files={"file": file})
    
with open("result.png", "wb") as fio:
    fio.write(r.content)```
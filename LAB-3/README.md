# TCC Case Study Task 3

## How to run:

1 Install dependencies

```bash
pip install -r requirements.txt
```

2 Add the **outputs** folder to the root of the LAB-3

3 Run the uvicorn server

```bash
cd src/
uvicorn main:app
```

4 Test the endpoint

```bash
curl -X POST http://localhost:8000/ -H 'Content-Type: application/json' -d '{"title":"baby"}'
```

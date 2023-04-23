# QR Codes REST API

## Description

This API allows you to generate QR code for your item(with name, description, price and image data). QR code contains
links to api to retrieve data and image for your usage(example is in qrcode_scanner folder)

## Installation

First of all you need to clone project

```commandline
git clone [add link here]
cd qrcodes_api
```

The next step is to create virtual environment for this project

```commandline
python -m venv venv
\venv\Scripts\activate
```

And install all dependencies

```commandline
cd backend
pip install -r requirements.txt
cd ..
```

## How to run

To run sever just use command below
```commandline
uvicorn backend.main:app
```

And go to link in your terminal

Add /docs to link you move from previous step

## How to create QR code

Open Add Item tab => Press try it out and fill all fields => press execute

If success you may see qr code in backend/images/qr_codes with name [item id].png


## How to try QR code scanner

Go to qrcode_scanner folder 

Install all dependencies

```commandline
pip install -r requirements.txt
```

and fill all fields in scan_qrcode.py

Then just run it

```commandline
python scan_qrcode.py
```
# Networth Tracker

## What does this project do?
Networth Tracker is a web application built with Django that helps users track their accounts and calculate their total net worth in one place. It is especially useful for combining asset information from multiple brokerage accounts. Because the code is open source, you can self-host it and keep your sensitive financial data under your own control instead of trusting a third-party provider. Users can manage their accounts and assets, fetch live market prices, and view everything converted into their preferred display currency.

### Main features
- **User authentication** – registration, login, logout, and account deletion.
- **Account management** – create, rename, and delete accounts (e.g., brokerage, savings, crypto).
- **Asset management** – add, edit (name, ticker, quantity, price), and delete assets inside each account.
- **Live market prices** – automatic price updates and currency conversion using Yahoo Finance (`yfinance`).
- **Display currency settings** – switch the main net worth currency (e.g., PLN, USD, EUR) at any time.

### Tech stack
- **Backend:** Python, Django
- **Database:** PostgreSQL
- **Frontend:** HTML, CSS, Vanilla JavaScript (Django Templates)
- **External API:** `yfinance` (Yahoo Finance)

---

## What does it look like?


### Dashboard (Accounts & Net Worth)
![Dashboard](screenshots/home.png)

### Account Details & Assets
![Account details](screenshots/account_detail.png)

---

## Where can I watch it live?
The live version of the app is available here:  
👉 **[Live Demo](https://app-url-here.com)**



---

## How do I run it?

### Prerequisites



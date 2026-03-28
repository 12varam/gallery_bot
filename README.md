# 📸 Telegram Gallery CRUD Bot

A robust and well-structured Telegram bot for managing your personal image collections. This bot allows you to create galleries, save photos with descriptions, and fully manage your content through an intuitive interface.

Built with the **aiogram 3.x** framework and powered by a **PostgreSQL** relational database.

## 🚀 Key Features

* **Gallery Management**: Create, rename, and delete custom galleries for your photos.
* **Smart Saving**: Add photos with custom descriptions or use the `/skip` command to save them without text.
* **Pagination System**: Browse your images in a clean list (10 items per page) with "Next/Prev" navigation buttons.
* **Full CRUD Functionality**:
    * **Create**: Easily add new galleries and photos.
    * **Read**: Browse your gallery list and view specific photo details.
    * **Update**: Replace an existing photo file or edit its description on the fly.
    * **Delete**: Remove individual photos or entire galleries (includes cascade deletion of all images within).

## 🛠 Tech Stack

* **Language:** [Python 3.10+](https://www.python.org/)
* **Framework:** [aiogram 3.x](https://docs.aiogram.dev/) (Asyncio)
* **Database:** [PostgreSQL](https://www.postgresql.org/)
* **Environment:** [environs](https://pypi.org/project/environs/) (for secure configuration)
* **DB Driver:** [psycopg2](https://pypi.org/project/psycopg2/) (Requires `libpq-dev` or similar on your OS)

## ⚙️ Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/UmarZeyn12/gallery_bot.git](https://github.com/UmarZeyn12/gallery_bot.git)
    cd gallery-bot
    ```

2.  **Configure Environment Variables:**
    Copy the example config and fill in your bot token and database credentials:
    ```bash
    cp .env.example .env
    ```

3.  **Install Dependencies:**
    *Note: Ensure you have PostgreSQL development headers installed on your system for psycopg2.*
    ```bash
    pip install -r requirements.txt
    ```

4.  **Prepare the Database:**
    Use the built-in utility to create the necessary tables:
    ```bash
    python -m utils.create_tables
    ```

5.  **Run the Bot:**
    ```bash
    python main.py
    ```

## 📂 Project Structure

```text
├── config/         # Environment configuration loading
├── database/       # PostgreSQL logic (connection, table schemas)
├── fsm/            # Finite State Machine definitions
├── handlers/       # Message and callback query handlers
├── keyboards/      # Inline and Reply keyboard generators
├── utils/          # Database administration scripts
└── main.py         # Application entry point
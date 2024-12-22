![SoundWish](https://raw.githubusercontent.com/tschuerti/SoundWish/4fa60ea3722149a5ccec98331162703c1cd7bc1e/media/logo.png)

SoundWish is a Flask-based web application that allows users to submit song requests for events. The application integrates with the Spotify API to search for songs and display track information.

## Features

- User authentication for event organizers
- Song request submission form
- Song search functionality using the Spotify API
- Overview of submitted, played, and deleted song requests
- QR code generation for event URLs


## Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/soundwish.git
    cd soundwish
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Create a  file in the root directory and add your Spotify API credentials:
    ```env
    CLIENT_ID=your_spotify_client_id
    CLIENT_SECRET=your_spotify_client_secret
    ```

5. Run the application:
    ```sh
    python main.py
    ```

## Usage

- Access the application at `http://localhost:5000`
- Navigate to the event URL (e.g., `http://localhost:5000/demo`)
- Submit song requests using the form
- Event organizers can log in to view and manage song requests

## License

This project is licensed under the MIT License. See the LICENSE file for details.
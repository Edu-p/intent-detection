>![DALL·E 2024-11-03 09 46 35 - A simple illustration of a human interacting with a chatbot  The person is seated at a desk with a minimalist screen displaying a chat interface, show](https://github.com/user-attachments/assets/efa9687a-190d-4894-98ef-7b8c3e6d5e5a)
>
 A chatbot designed to predict user intentions and interact with a database to retrieve the last three intents.
## What is the project?

This project is an **Intent Detection Chatbot** that predicts user intentions and interacts with a MongoDB database to retrieve the last three user intents. The chatbot provides an interactive interface for users, enhancing engagement by understanding and responding to their needs effectively.

## Demo
![demo](https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExMnNocGYxbnhycGFrdGNqMzZ4aWNtOGt4dWM1OTlqdmpnanZyeWZzMSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/gVe9Z1bTD7OTSk569b/giphy.gif)

## Technical Description

The project is developed using:

- **Frontend**: [Streamlit](https://streamlit.io/) for a user-friendly web interface.
- **Backend**: [Flask](https://flask.palletsprojects.com/) to handle API requests and business logic.
- **Database**: [MongoDB](https://www.mongodb.com/) for storing and retrieving user intents.

## Project Structure

The project is organized as follows:

- **`notebooks`**: Contains Jupyter notebooks used for **deep evaluation of the model**, **studies on finding the best threshold** to consider non-valid responses, and scripts used for **fine-tuning the DistilBERT model**.

- **`flask_back/routes`**: Contains a single route `/chat` that makes predictions using the fine-tuned `'distilbert-base-uncased'` model.

- **`flask_back/rsc`**: Includes resources like the tokenizer, datasets used during training, test datasets, and an example of the database.
   - download model.safetensors and the tokenizer from this: [model rsc](https://drive.google.com/drive/folders/1RjpoTNWcwxrOyFTdtrsn92JrN0nJN-37?usp=sharing)  

- **`streamlit_front/pages`**: Holds the single page that allows users to interact with the chatbot via the Streamlit interface.

## How to Execute the Project

Follow the steps below to set up and run the project locally.

### Prerequisites

- **Python >3.10** installed on your machine.
- **MongoDB** installed locally or access to a MongoDB Atlas cluster.
- **pip** package manager.

### Environment Variables

Create environment variable files for both the frontend and backend to store sensitive information.

#### Frontend (`streamlit_front/.env`)

- **BASE_URL**: The base URL where the backend is running (e.g., `http://localhost:5000`).

#### Backend (`flask_back/.env`)

- **MONGO_URI**: The connection string for your MongoDB database. (e.g., `"mongodb://localhost:27017"`).

### Setting Up Environment Variables

```bash
# Navigate to the project directories
$ cd streamlit_front
$ touch .env
$ cd ../flask_back
$ touch .env
```



### Installing Dependencies
Install the required Python packages for both frontend and backend.

```bash
# Navigate to the project root directory
$ cd ..

# Install dependencies
$ pip install -r requirements.txt
```

### Running the Backend
Start the Flask backend server.

```bash
# Navigate to the backend directory
$ cd flask_back

# Run the Flask app
$ python app.py
```

### Running the Frontend
In a new terminal window, start the Streamlit frontend.

```bash
# Navigate to the backend directory
$ cd flask_back

# Run the Flask app
$ python app.py
```
The frontend should now be accessible at http://localhost:8501

### Database Setup
The example database dump is located at flask_back/rsc/mongodump/dbIntents. Use this to populate your MongoDB database.

```bash
# Restore the MongoDB dump
$ mongorestore --uri your_mongo_uri flask_back/rsc/mongodump/dbIntents
```
Replace your_mongo_uri with your actual MongoDB connection string.



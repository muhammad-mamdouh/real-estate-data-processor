# Real Estate App

> A real estate web app that implements two API endpoints one for uploading the portfolio data
> and the other one for retrieving aggregate information about assets.


# Table of contents
1. [Stack Used](#stack-used)
2. [Usage](#usage)
3. [Requirements](#requirements)
4. [Build the docker image](#build-the-docker-image)
5. [Run the development server using docker compose](#run-the-development-server-using-docker-compose)
6. [Run the Test Cases](#run-the-test-cases)
7. [Test the Upload File API Endpoint](#test-the-upload-file-api-endpoint)
8. [Check Your Uploaded Data Representation From the Django Admin Panel](#check-your-uploaded-data-representation-from-the-django-admin-panel)
9. [Test the Assets Info Aggregation API Endpoint](#test-the-assets-info-aggregation-api-endpoint)
10. [License](#license)


## Stack Used

1. Docker v. 19.03.12
2. Docker Compose v. 1.26.0
3. PostgreSQL v. 12.0
4. RabbitMQ v. 3.8
5. Django Web Framework v. 3.0
6. Django Rest Framework for implementing API endpoints v. 3.11
7. Celery v. 4.4.6 for Asynchronous tasks


## Usage

To be able to make this app up and running follow along with me.


## Requirements

1. docker v. 19.03.12
2. docker-compose v. 1.26.0
    . Link for installation https://docs.docker.com/engine/install/
3. Terminal


## Build the docker image

```
# From your terminal, extract code_challenge.zip and cd into the code_challenge directory

docker-compose build
```


## Run the development server using docker compose

```
# After the build is finished with a success message you're good to go to make the server up and running

docker-compose up
```


## Run the Test Cases
```
# From your terminal, within the same code_challenge directory

docker-compose exec app python manage.py test
```


## Test the Upload File API Endpoint

* Open your favorite browser and open the link below
    ```
    http://localhost:8000/api/secure/v1/upload/
    ```
* Click on the Choose File and choose your portfolio data sheet
* Click on POST
* Now you'll find that the sheet is uploaded successfully and passed for processing
* You'll receive an email after the file processing is finished
    ```
    Go to the env dir, open the .env.dev and change the MAIL_RECEIVER to your email
    to reveive the file processing status follow up email.
    ```

```
# Response Sample

HTTP 201 Created
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json

{
    "File Uploaded": {
        "file": "http://localhost:8000/media/documents/2020/7/30/units_20190101__HB72X8IHG0.csv"
    },
    "Status": "File is validated successfully and is being processed now, you'll receive a follow up email whenever the processing is completed!"
}
```


## Check Your Uploaded Data Representation From the Django Admin Panel

1. Create an administrator user, run the following command adding your username and your password
```
# From your terminal, within the same code_challenge directory

docker-compose exec app python manage.py createsuperuser
```

2. Go to your browser and open the following link using your credentials
```
http://localhost:8000/admin/
```

3. You'll find a link for every database table with the name of the model 


## Test the Assets Info Aggregation API Endpoint

1. Show the full assets info aggregation list
```
# Keep in mind that the requests made to this endpoint are paginated

# From your browser
http://localhost:8000/api/secure/v1/assets/

# Or from your terminal, within the same code_challenge directory
docker-compose exec app http GET :8000/api/secure/v1/assets/
```

2. Show aggregated info about specific asset
```
# From your terminal, within the same code_challenge directory
docker-compose exec app http GET :8000/api/secure/v1/assets/ asset_ref=A_1
```

```
# Response Sample

HTTP/1.0 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json

{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "address": "Am Kupfergraben 6",
            "area_rented": 650,
            "city": "Berlin",
            "latest_update": "30.07.2020",
            "number_of_units": 6,
            "restricted_area": true,
            "total_area": 745,
            "total_rent": 6600.0,
            "vacancy": "16.67 %",
            "walt": "4.9 years",
            "year_of_construction": 1876,
            "zipcode": 10117
        }
    ]
}
```


## License
These projects are under [The license License](LICENSE).

# cloudrun-cloudsql
gcloud builds submit --tag us-central1-docker.pkg.dev/PROJECT_ID/login-repo/login-app:v1
create table:
CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(100),
  email VARCHAR(100),
  login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

users list:
SELECT * FROM users;

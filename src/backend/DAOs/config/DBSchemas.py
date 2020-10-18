
CREATE TABLE accounts (
	user_id serial PRIMARY KEY,
	username VARCHAR ( 50 ) UNIQUE NOT NULL,
	password VARCHAR ( 50 ) NOT NULL,
	first_name VARCHAR,
	last_name VARCHAR,
	email VARCHAR ( 255 ) UNIQUE NOT NULL,
	is_recruiter BOOLEAN NOT NULL
);

CREATE TABLE resumes (
	resume_data BYTEA NOT NULL,
	resume_extension VARCHAR(10) NOT NULL,
	education VARCHAR(60) NOT NULL,
	college_name VARCHAR(60) NOT NULL,
	degree VARCHAR(60) NOT NULL,
	designation VARCHAR(60) NOT NULL,
	experience VARCHAR(60) NOT NULL,
	company_names VARCHAR(60) NOT NULL,
	skills VARCHAR(200) NOT NULL,
	total_experience DECIMAL NOT NULL,
	last_updated TIMESTAMP NOT NULL,
	user_id int UNIQUE NOT NULL,
	PRIMARY KEY ( user_id ),
	FOREIGN KEY ( user_id ) REFERENCES accounts( user_id )
);

CREATE TABLE jobPostings (
	posting_id serial PRIMARY KEY,
	position_name VARCHAR ( 50 ) NOT NULL,
	location VARCHAR ( 50 ) NOT NULL,
	description VARCHAR (300),
	key_details VARCHAR ( 500 ),
	pay_type VARCHAR ( 50 ) NOT NULL,
	pay_amount INT NOT NULL,
	user_id INT NOT NULL,
	deadline TIMESTAMP  NOT NULL,
	presentationDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY ( user_id ) REFERENCES accounts( user_id )
);

CREATE TABLE applications (
	user_id INT NOT NULL,
	posting_id INT NOT NULL,
	rank INT NOT NULL,
	PRIMARY KEY (user_id, posting_id),
	FOREIGN KEY (user_id) REFERENCES accounts(user_id),
	FOREIGN KEY (posting_id) REFERENCES jobPostings(posting_id)
);
passcode_form = """<!DOCTYPE html>
<html>
<head>
    <title>Swagger Access</title>
    <style>
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            font-family: Arial, sans-serif;
            background-color: #fafafa;
        }
        form {
            border: 1px solid #ddd;
            padding: 20px;
            border-radius: 5px;
            background: white;
            box-shadow: 0 2px 4px rgba(0,0,0,.1);
        }
        input[type="password"], input[type="submit"] {
            margin-top: 10px;
            margin-right: 5px;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        input[type="submit"] {
            cursor: pointer;
            background-color: #007bff;
            color: white;
            border: 1px solid #007bff;
        }
        input[type="submit"]:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>
    <form method="post">Enter passcode: <input name="passcode" type="password" />
    <input type="submit" /></form>
</body>
</html>
"""

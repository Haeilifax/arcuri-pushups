import boto3
import urllib.parse
from http import cookies
from jinja2 import Environment, PackageLoader, select_autoescape
import base64
import importlib.resources

TABLENAME = "Arcuri-Pushups-store"

def lambda_handler(event, context):
    ddb = boto3.client("dynamodb")
    method = event["requestContext"]["http"]["method"]
    path = event["requestContext"]["http"]["path"]
    event_cookies = event.get("cookies", [])
    username = ''
    for cookie in event_cookies:
        cookie_morsel = cookies.SimpleCookie(cookie)
        if cookie_morsel.get("UserName") is not None:
            username = cookie_morsel.get("UserName").value
            break
    if method == "GET":
        if path == "/stylesheet.css":
            # Serve CSS file
            print("Serving CSS file")
            css_content = importlib.resources.files().joinpath(
                "templates", "stylesheet.css"
            ).read_text()
            return {
                "statusCode": 200,
                "headers": {"Content-Type": "text/css"},
                "body": css_content,
            }
        all_ddb_items = ddb.scan(TableName=TABLENAME, ProjectionExpression="UserName,Pushups")["Items"]
        all_pushups = {}
        for item in all_ddb_items:
            item_username = None
            item_pushups = None
            for attribute, value in item.items():
                if attribute == "UserName":
                    item_username = value["S"]
                elif attribute == "Pushups":
                    item_pushups = value["N"]
            if item_username is not None and item_pushups is not None:
                all_pushups[item_username.capitalize()] = item_pushups
            else:
                print(f"Could not find: {'UserName' if not item_username else ''} {'Pushups' if not item_pushups else ''} for {item}")
        env = Environment(
            loader=PackageLoader("pushups"), autoescape=select_autoescape()
        )
        template = env.get_template("index.jinja")
        resp = {
            "statusCode": 200,
            "headers": {"Content-Type": "text/html"},
            "body": template.render({"all_pushups": all_pushups, "username": username.capitalize()}),
        }
        print(resp)
        return resp
    if method == "POST":
        # Parse form data from request body
        body = event.get("body", "")
        if event.get("isBase64Encoded"):
            body = base64.b64decode(body).decode("utf-8")
        form_data = urllib.parse.parse_qs(body)
        pushups = form_data["pushups"][0]
        username = form_data["username"][0].capitalize()
        ddb.update_item(TableName=TABLENAME, Key={"UserName":{"S":username}}, UpdateExpression="ADD Pushups :pushups", ExpressionAttributeValues={":pushups":{"N":pushups}})
        resp = {
            "statusCode": 303,
            "headers": {"Set-Cookie": f"UserName={username};", "Location": "/"}
        }
        return resp

if __name__ == "__main__":
    lambda_handler({"requestContext":{"http":{"path":"/", "method":"GET"}}, "cookies":["UserName=David;"]}, None)
    # lambda_handler({"requestContext":{"http":{"path":"/", "method":"POST"}}, "cookies":["UserName=David;"], "body":"pushups=20"}, None)
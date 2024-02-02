from restApiDb.restApi import RestApi

server = RestApi()
app = server.app
if __name__ == "__main__":
    app.run()

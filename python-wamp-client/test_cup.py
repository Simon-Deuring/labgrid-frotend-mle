    # from autobahn.asyncio.component import Component,run

    # component = Component(
    #     transports = u"ws://dummy@localhost:5901/mle-lg-ref-1",
    #     realm='mle-lg-ref-1'
    # )

    # @component.on_connect
    # def onConnect():
    #     print("connecting")

    # @component.on_join
    # def onJoin(session, details):
    #     print("joined")


    # if __name__ == '__main__':
    #     run([component])


from autobahn.twisted.component import Component, run
from autobahn.wamp.types import RegisterOptions
from autobahn.wamp.exception import ApplicationError
from twisted.internet.defer import inlineCallbacks


@inlineCallbacks
def main(reactor, session):
    print("Client session={}".format(session))

    try:
        res = yield session.register(lambda: None, "com.foo.private")
        print("\n\nregistering 'com.foo.private' should have failed\n\n")
    except ApplicationError as e:
        print("registering 'com.foo.private' failed as expected: {}".format(e.error))

    res = yield session.register(
        lambda: None, "should.work",
        options=RegisterOptions(match='exact'),
    )
    print("registered 'should.work' with id {}".format(res.id))

    try:
        res = yield session.register(
            lambda: None, "prefix.fail.",
            options=RegisterOptions(match='prefix'),
        )
        print("\n\nshould have failed\n\n")
    except ApplicationError as e:
        print("prefix-match 'prefix.fail.' failed as expected: {}".format(e.error))

    print("calling 'example.foo'")
    try:
        res = yield session.call("example.foo")
    except Exception as e:
        # to see errors uncomment the "throw" in backend .. also try
        # with .traceback_app enabled (in the backend)
        print("Error from 'example.foo' call:")
        print(e)
    print("example.foo() = {}".format(res))

    print("done")


component = Component(
    transports="ws://localhost:5901/cup",
    main=main,
    realm="realm1",
    # authentication={
    #     "wampcra": {
    #         "authid": "bob",
    #         "authrole": "dynamic_authed",
    #         "secret": "p4ssw0rd",
    #     }
    # }
)


if __name__ == "__main__":
    run([component])
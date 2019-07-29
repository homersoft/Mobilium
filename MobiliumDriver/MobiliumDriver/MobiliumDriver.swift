//
//  MobiliumDriver.swift
//  MobiliumDriver
//
//  Created by Marek Niedbach on 21/05/2019.
//  Copyright © 2019 Silvair. All rights reserved.
//

import XCTest
import Network
import SocketIO

class MobiliumDriver: XCTestCase, StreamDelegate {
    var socket: SocketIOClient?
    var deserializer = MessageDeserializer()
    var keepAlive = true

    func testApplication() {
        guard let host = ProcessInfo.processInfo.environment["HOST"],
            let port = ProcessInfo.processInfo.environment["PORT"] else { return XCTFail("Host or port not provided") }

        let manager = SocketManager(socketURL: URL(string: "tcp://\(host):\(port)")!, config: [.log(true), .compress])
        socket = manager.socket(forNamespace: "/driver")

        socket?.on(clientEvent: .connect) { [weak self] (data, ack) in
            let data = MessageDataFactory.startDriverResponse()
            self?.socket?.emit("message", with: [data])
        }
        socket?.on(clientEvent: .disconnect) { [weak self] (data, ack) in
            self?.keepAlive = false
        }
        socket?.on("message") { [weak self] (data, ack) in
            guard let data = data as? [Data] else { return }

            if self?.deserializer.executeTestRequest(from: data) != nil {
                self?.executeTest()
            }
        }
        socket?.connect()

        while keepAlive && RunLoop.main.run(mode: .default, before: .distantFuture) { }
    }

    func executeTest() {
        continueAfterFailure = true

        let app = XCUIApplication(bundleIdentifier: "com.silvair.commissioning.test.dev")
        app.launch()

        Thread.sleep(forTimeInterval: 1.0)

        app.terminate()
        socket?.emit("message", "TestExecuted")

        Thread.sleep(forTimeInterval: 1.0)
        socket?.disconnect()
    }
}


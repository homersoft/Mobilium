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

let ip = "192.168.52.93"
let port = 65432


class MobiliumDriver: XCTestCase, StreamDelegate {
    var socket: SocketIOClient?
    var keepAlive = true

    func testApplication() {
        let manager = SocketManager(socketURL: URL(string: "tcp://\(ip):\(port)")!, config: [.log(true), .compress])
        socket = manager.socket(forNamespace: "/driver")

        socket?.on(clientEvent: .connect) { [weak self] (data, ack) in
            self?.socket?.emit("message", with: ["DriverStarted"])
        }
        socket?.on(clientEvent: .disconnect) { [weak self] (data, ack) in
            self?.keepAlive = false
        }
        socket?.on("message") { [weak self] (data, ack) in
            if data.first as? String == "ExecuteTest" {
                self?.executeTest()
            }
        }
        socket?.connect()

        while keepAlive && RunLoop.main.run(mode: .default, before: .distantFuture) {}
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


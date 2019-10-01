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
    var app: XCUIApplication!
    var socket: SocketIOClient?
    var deserializer = MessageDeserializer()
    var keepAlive = true

    func testApplication() {
        guard let host = ProcessInfo.processInfo.environment["HOST"],
            let port = ProcessInfo.processInfo.environment["PORT"] else { return XCTFail("Host or port not provided") }

        let manager = SocketManager(socketURL: URL(string: "tcp://\(host):\(port)")!, config: [.log(true), .compress])
        socket = manager.socket(forNamespace: "/driver")

        socket?.on(clientEvent: .connect) { [weak self] (data, ack) in
            print("Driver socket connected!")
            let data = MessageDataFactory.startDriverResponse()
            self?.socket?.send(message: data)
        }
        socket?.on(clientEvent: .disconnect) { [weak self] (data, ack) in
            print("Driver socket disconnected!")
            self?.keepAlive = false
        }
        socket?.on("message") { [weak self] (data, ack) in
            print("Driver did receive message")
            guard let data = data as? [Data] else { return }

            if let message = self?.deserializer.launchAppRequest(from: data) {
                self?.launchApp(bundleId: message.bundleID)
            }

            if let message = self?.deserializer.isElementVisibileRequest(from: data) {
                self?.checkElementVisible(with: message.accessibilityID, timeout: TimeInterval(message.timeout))
            }
            
            if let message = self?.deserializer.getValueOfElementRequest(from: data) {
                self?.readValueOfElement(with: message.accessibilityID)
            }
            
            if let message = self?.deserializer.setValueOfElementRequest(from: data) {
                self?.setValueOfElementUsingMessage(message)
            }
            
            if let message = self?.deserializer.clickElementRequest(from: data) {
                self?.clickElement(with: message.accessibilityID)
            }
            
            if let _ = self?.deserializer.terminateAppRequest(from: data) {
                self?.terminateApp()
            }
        }
        print("Driver socket connection attempt")
        socket?.connect()

        while keepAlive && RunLoop.main.run(mode: .default, before: .distantFuture) { }
    }


    private func launchApp(bundleId: String) {
        continueAfterFailure = true

        app = XCUIApplication(bundleIdentifier: bundleId)
        app.launch()

        Thread.sleep(forTimeInterval: 1.0)

        let data = MessageDataFactory.appLaunchResponse()
        socket?.send(message: data)
    }

    private func terminateApp() {
        app.terminate()

        let messageData = MessageDataFactory.terminateAppResponse()
        socket?.send(message: messageData)
    }

    private func checkElementVisible(with accessibilityId: String, timeout: TimeInterval) {
        let element = app.element(with: accessibilityId)
        let elementExists = element.waitForExistence(timeout: timeout)

        let messageData = MessageDataFactory.isElementVisibleResponse(accessibilityId: accessibilityId, exists: elementExists)
        socket?.send(message: messageData)
    }
    
    private func clickElement(with accessibilityId: String) {
        let element = app.element(with: accessibilityId)
        let elementExists = element.exists
        if elementExists {
            element.tap()
        }
        
        let messageData = MessageDataFactory.clickElementResponse(accessibilityId: accessibilityId, exists: elementExists)
        socket?.send(message: messageData)
    }
    
    private func readValueOfElement(with accessibilityId: String) {
        let element = app.element(with: accessibilityId)
        guard element.exists else {
            let messageData = MessageDataFactory.getValueOfElementResponse(accessibilityId: accessibilityId,
                                                                           exists: false, value: nil)
            socket?.send(message: messageData)
            return
        }

        let value = element.value as? String ?? element.label
        let messageData = MessageDataFactory.getValueOfElementResponse(accessibilityId: accessibilityId,
                                                                       exists: true, value: value)
        socket?.send(message: messageData)
    }
    
    private func setValueOfElementUsingMessage(_ message: SetValueOfElementRequest) {
        let element = app.element(with: message.accessibilityID)
        guard element.exists else {
            let messageData = MessageDataFactory.setValueOfElementResponse(accessibilityId: message.accessibilityID,
                                                                           exists: false)
            socket?.send(message: messageData)
            return
        }

        switch message.value {
        case .text(let newTextValue)?:
            element.setText(newTextValue.value, replace: newTextValue.clears)
        case .position(let newPosition)?:
            element.adjust(toNormalizedSliderPosition: CGFloat(newPosition))
        case .selection(let newValue)?:
            element.setSelection(to: newValue)
        default:
            print("Invalid message send to driver. Message: \(String(describing: message))")
        }
        
        let messageData = MessageDataFactory.setValueOfElementResponse(accessibilityId: message.accessibilityID,
                                                                       exists: true)
        socket?.send(message: messageData)
    }
}

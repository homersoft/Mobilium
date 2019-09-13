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
            let data = MessageDataFactory.startDriverResponse()
            self?.socket?.emit("message", with: [data])
        }
        socket?.on(clientEvent: .disconnect) { [weak self] (data, ack) in
            self?.keepAlive = false
        }
        socket?.on("message") { [weak self] (data, ack) in
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
        socket?.connect()

        while keepAlive && RunLoop.main.run(mode: .default, before: .distantFuture) { }
    }


    private func launchApp(bundleId: String) {
        continueAfterFailure = true

        app = XCUIApplication(bundleIdentifier: bundleId)
        app.launch()

        Thread.sleep(forTimeInterval: 1.0)

        let data = MessageDataFactory.appLaunchResponse()
        socket?.emit("message", with: [data])
    }

    private func terminateApp() {
        app.terminate()

        let messageData = MessageDataFactory.terminateAppResponse()
        socket?.emit("message", with: [messageData])
    }

    private func checkElementVisible(with accessibilityID: String, timeout: TimeInterval) {
        let element = app.element(with: accessibilityID)
        let elementExists = element.waitForExistence(timeout: timeout)

        let messageData = MessageDataFactory.isElementVisibleResponse(accessibilityId: accessibilityID, isVisible: elementExists)
        socket?.emit("message", with: [messageData])
    }
    
    private func clickElement(with accessibilityID: String) {
        let element = app.element(with: accessibilityID)
        if element.exists {
            element.tap()
        }
        
        let messageData = MessageDataFactory.clickElementResponse(accessibilityId: accessibilityID)
        socket?.emit("message", with: [messageData])
    }
    
    private func readValueOfElement(with accessibilityID: String) {
        let element = app.element(with: accessibilityID)
        var value: String?
        
        if element.exists {
            value = element.value as? String ?? element.label
        }
        let messageData = MessageDataFactory.getValueOfElementResponse(accessibilityId: accessibilityID, value: value)
        socket?.emit("message", messageData)
    }
    
    private func setValueOfElementUsingMessage(_ message: SetValueOfElementRequest) {
        let element = app.element(with: message.accessibilityID)
        switch element.elementType {
        case .checkBox:
            setSelectionOfCheckboxElement(element, to: message.selection)
        case .textField, .textView, .secureTextField:
            setTextOnTextElement(element, to: message.text)
        case .slider:
            setSliderElementPosition(element, to: message.position)
        case .pickerWheel:
            setPickerWheelElementPosition(element, to: message.text)
        default:
            break // emit error
        }
        
        let messageData = MessageDataFactory.setValueOfElementResponse(accessibilityId: message.accessibilityID)
        socket?.emit("message", messageData)
    }
    
    private func setTextOnTextElement(_ element: XCUIElement, to newText: String) {
        guard element.exists else { return }
        
        element.tap()
        element.replaceText(with: newText)
        app.hideKeyboard()
    }
    
    private func setSliderElementPosition(_ element: XCUIElement, to newPosition: Float) {
        guard element.exists else { return }
        
        element.adjust(toNormalizedSliderPosition: CGFloat(newPosition))
    }
    
    private func setPickerWheelElementPosition(_ element: XCUIElement, to pickerValue: String) {
        guard element.exists else { return }
        
        element.adjust(toPickerWheelValue: pickerValue)
    }
    
    private func setSelectionOfCheckboxElement(_ element: XCUIElement, to newValue: Bool) {
        guard element.exists, element.isSelected != newValue else { return }
        
        element.tap()
    }
}


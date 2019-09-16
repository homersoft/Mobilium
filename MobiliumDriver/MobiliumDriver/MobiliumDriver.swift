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
            
            if let message = self?.deserializer.hideKeyboardRequest(from: data) {
                self?.hideKeyboard()
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
        socket?.send(message: data)
    }

    private func terminateApp() {
        app.terminate()

        let messageData = MessageDataFactory.terminateAppResponse()
        socket?.send(message: messageData)
    }
    
    private func hideKeyboard() {
        app.hideKeyboard()
        
        let messageData = MessageDataFactory.hideKeyboardResponse()
        socket?.emit("message", messageData)
    }

    private func checkElementVisible(with accessibilityID: String, timeout: TimeInterval) {
        let element = app.element(with: accessibilityID)
        let elementExists = element.waitForExistence(timeout: timeout)

        let messageData = MessageDataFactory.isElementVisibleResponse(accessibilityId: accessibilityID, isVisible: elementExists)
        socket?.send(message: messageData)
    }
    
    private func clickElement(with accessibilityID: String) {
        let element = app.element(with: accessibilityID)
        if element.exists {
            element.tap()
        }
        
        let messageData = MessageDataFactory.clickElementResponse(accessibilityId: accessibilityID)
        socket?.send(message: messageData)
    }
    
    private func readValueOfElement(with accessibilityID: String) {
        let element = app.element(with: accessibilityID)
        var value: String?
        
        if element.exists {
            value = element.value as? String ?? element.label
        }
        let messageData = MessageDataFactory.getValueOfElementResponse(accessibilityId: accessibilityID, value: value)
        socket?.send(message: messageData)
    }
    
    private func setValueOfElementUsingMessage(_ message: SetValueOfElementRequest) {
        let element = app.element(with: message.accessibilityID)
        
        switch message.value {
        case .text(let newTextValue)?:
            setTextOnTextElement(element, to: newTextValue.value, withClearing: newTextValue.clears)
        case .position(let newPosition)?:
            setSliderElementPosition(element, to: newPosition)
        case .selection(let newSelectionValue)?:
            setSelectionOfCheckboxElement(element, to: newSelectionValue)
        default:
            break // emit error
        }
        
        let messageData = MessageDataFactory.setValueOfElementResponse(accessibilityId: message.accessibilityID)
        socket?.emit("message", messageData)
    }
    
    private func setTextOnTextElement(_ element: XCUIElement, to newText: String, withClearing shouldClear: Bool) {
        guard element.exists else { return }
        
        element.tap()
        if shouldClear {
            element.replaceText(with: newText)
        } else {
            element.typeText(newText)
        }
    }
    
    private func setSliderElementPosition(_ element: XCUIElement, to newPosition: Float) {
        guard element.exists else { return }
        
        element.adjust(toNormalizedSliderPosition: CGFloat(newPosition))
    }
    
    private func setPickerWheelElementPosition(_ element: XCUIElement, to pickerValue: String) {
        guard element.exists else { return }
        
        element.adjust(toPickerWheelValue: pickerValue)
    }
    
    private func setSelectionOfCheckboxElement(_ element: XCUIElement, to desirableSelectionState: Bool) {
        guard element.exists, let currentValue = element.value as? String else { return }
        
        let isSelected = Int(currentValue) == 1
        if isSelected != desirableSelectionState {
            element.tap()
        }
    }
}

